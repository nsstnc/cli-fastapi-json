from jinja2 import Template

class RouterGenerator:
    def __init__(self, model_name):
        self.model_name = model_name

    def render_router(self):
        template_str = open('cli/router_template.py.jinja').read()
        template = Template(template_str)
        return template.render(model_name=self.model_name)
