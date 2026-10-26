import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
import json
import os
import sys

from fastmcp import Client
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route
import uvicorn

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parents[1]
lock = asyncio.Lock()


@asynccontextmanager
async def lifespan(app):
    config = {"mcpServers": {"game": {
        "command": str(Path(sys.executable).parent / ('career-emulator-engine-mcp.exe' if os.name == 'nt' else 'career-emulator-engine-mcp')),
        "args": ['--update', 'skip'],
    }}}
    async with Client(config) as client:
        app.state.client = client
        yield


async def home(request):
    return FileResponse(ROOT / 'index.html')


async def api(request: Request):
    origin = request.headers.get('origin')
    if origin and origin != f"http://{request.headers.get('host')}":
        return JSONResponse({'error': 'Origin not allowed'}, status_code=403)
    try:
        body = await request.json()
        operation = request.path_params['operation']
        args = {}
        mapping = {'new': 'new_game', 'observe': 'observe',
                   'action': 'take_action', 'logs': 'check_latest_logs',
                   'handbook': 'show_employee_handbook'}
        if operation not in mapping:
            return JSONResponse({'error': 'Unknown operation'}, status_code=404)
        if operation in ('observe', 'action', 'logs'):
            args['session_id'] = body['session_id']
        if operation == 'action':
            if type(body.get('choice')) is not int:
                raise ValueError('Choice must be an integer')
            args.update(choice=body['choice'], notes=body.get('notes', ''))
        if operation == 'logs':
            args['count'] = 30
        async with lock:
            result = await request.app.state.client.call_tool(mapping[operation], args)
        if result.is_error:
            raise ValueError(str(result.content))
        data = result.data
        if data is None:
            data = '\n'.join(getattr(c, 'text', '') for c in result.content)
            try:
                data = json.loads(data)
            except (ValueError, TypeError):
                pass
        return JSONResponse({'data': data})
    except Exception as exc:
        return JSONResponse({'error': str(exc)}, status_code=400)


app = Starlette(routes=[Route('/', home), Route('/api/{operation}', api, methods=['POST'])], lifespan=lifespan)

if __name__ == '__main__':
    os.chdir(BASE)
    uvicorn.run(app, host='127.0.0.1', port=8765)
