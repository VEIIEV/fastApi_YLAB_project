# # -- FILE: features/environment.py
# import threading
# from behave.model import Feature, Scenario
# from wsgiref import simple_server
#
# from behave.fixture import fixture, use_fixture_by_tag
#
# @fixture
# def webserver(context):
#     # -- STEP: Setup browser fixture
#     context.server = simple_server.WSGIServer(("", 8000))
#     context.server.set_app(web_app.main(environment='test'))
#     context.thread = threading.Thread(target=context.server.serve_forever)
#     context.thread.start()
#     yield context.server
#     # -- STEP: Teardown/cleanup fixture
#     context.server.shutdown()
#     context.thread.join()
#
# @fixture
# def browser_chrome(context):
#     # -- STEP: Setup browser fixture
#     context.browser = webdriver.Chrome()
#     yield context.browser
#     # -- STEP: Teardown/cleanup fixture
#     context.browser.quit()
#
#
# fixture_registry = {
#     "fixture.browser":   browser_chrome,
#     "fixture.webserver": webserver,
# }
#
# # -- BEHAVE HOOKS:
# def before_feature(context, feature):
#     a=feature.
#     model.init(environment='test')
#
# def before_tag(context, tag):
#     if tag.startswith("fixture."):
#         # USE-FIXTURE FOR TAGS: @fixture.browser, @fixture.webserver
#         return use_fixture_by_tag(tag, context, fixture_registry):