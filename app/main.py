from .routers import apiPage, apiPage2

### Fixed FastAPI UI to normal
from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html
def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and 
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui.min.css")
applications.get_swagger_ui_html = swagger_monkey_patch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="AssetsX-API")

# Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API for API Page 1
app.include_router(
    apiPage.router,
    tags=["apiPage"],
)

# API for API Page 2
app.include_router(
    apiPage2.router,
    tags=["apiPage2"],    
)
