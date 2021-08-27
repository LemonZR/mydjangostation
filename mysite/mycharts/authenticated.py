from django.shortcuts import redirect, reverse


def is_authenticated(fn):
    def inner(request, *args, **kwargs):
        status = request.session.get('user')
        if status:
            ret = fn(request, *args, **kwargs)
            return ret
        else:
            request.session['HTTP_REFERER'] = request.get_full_path()
            return redirect(reverse('login'))

    return inner


def class_method_authenticated(fn):
    def inner(self, request, *args, **kwargs):
        status = request.session.get('user')
        if status:
            ret = fn(self, request, *args, **kwargs)
            return ret
        else:
            request.session.setdefault('HTTP_REFERER', request.get_full_path())
            return redirect(reverse('login'))

    return inner
