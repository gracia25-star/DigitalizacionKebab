return self.wsgi_app(environ, start_response)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1458, in wsgi_app
response = self.handle_exception(e)
           ^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1455, in wsgi_app
response = self.full_dispatch_request()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 869, in full_dispatch_request
rv = self.handle_user_exception(e)
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Open an interactive python shell in this frame
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 867, in full_dispatch_request
rv = self.dispatch_request()
     ^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 852, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\Desktop\PRACTICAS\Digitalización\Kit Digital\MegaDonerKebab\admin_app.py", line 45, in admin_index
return render_template('worker.html', username=session.get('username'))
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 152, in render_template
return _render(app, template, context)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 133, in _render
rv = template.render(context)
     ^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1295, in render
self.environment.handle_exception()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 942, in handle_exception
raise rewrite_traceback_stack(source=source)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\Desktop\PRACTICAS\Digitalización\Kit Digital\MegaDonerKebab\templates\worker.html", line 602, in top-level template code
<button class="btn-logout" onclick="window.location.href='{{ url_for('logout') }}'">
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1071, in url_for
return self.handle_url_build_error(error, endpoint, values)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1060, in url_for
rv = url_adapter.build(  # type: ignore[union-attr]
     
File "C:\Users\Mario\AppData\Roaming\Python\Python314\site-packages\werkzeug\routing\map.py", line 919, in build
raise BuildError(endpoint, values, method, self)