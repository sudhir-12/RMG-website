
from django.template import RequestContext
from django.shortcuts import render_to_response
from rmgweb.regression_tests.models import RegressionTestJob
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect

TIME_TO_SEARCH = 5.0

def index(request):
    """
    The RMG regression tests homepage.
    """
    # TODO: query db for job queue and render
    jobs = RegressionTestJob.objects.all()[::-1][0:10]
    return render_to_response('regression_tests.html',{'jobs': jobs}, context_instance=RequestContext(request))


@csrf_protect
@ensure_csrf_cookie
def add_job(request):
    if request.method == 'POST':
        rmgpy_branch = request.POST['autocompleteField_py']
        rmgdb_branch = request.POST['autocompleteField_db']
        job = RegressionTestJob.objects.create(rmgpy_branch=rmgpy_branch, rmgdb_branch=rmgdb_branch)
        job.job_status = '/media/wait.png'
        job.save()
        test = rmgpy_branch+'--'+rmgdb_branch
        spawn_test_job(rmgpy_branch, rmgdb_branch,job, request)
        return redirect('/regression_tests')
    else:
        return redirect('/regression_tests')


def spawn_test_job(rmgpy_branch, rmgdb_branch,job, request):

    import subprocess
    import os
    import time
    import threading


    command = 'echo spawning job > testing.txt'


    threading.Timer(TIME_TO_SEARCH, file_exists,args=(rmgpy_branch, rmgdb_branch, job, request)).start()

    os.system(command)
    #time.sleep(12
	# import subprocess
    # import os
    # command = 'Spawning job'
	# jobs = rmgpy_branch+'_'+rmgdb_branch
	# rmg_tests_script = os.path.join(os.environ["RMGTESTS"], 'local_tests', 'exe.sh')
	# command = ['bash',
	#            rmg_tests_script,
	#            rmgpy_branch,
	#            rmgdb_branch,
	#            jobs]

	#subprocess.Popen(command)

def file_exists(rmgpy, rmgdb, job, request):

    import os
    import threading
    command = "[ -f testing.txt ] && echo 'Found' || echo 'Not found'"
    is_found = os.popen(command).read().strip()
    test = rmgpy+'--'+rmgdb

    os.system('echo '+is_found)
    if(is_found == 'Found'):
        os.system('echo "The file has been found"')
        job.job_status = '/media/done.jpg'
        job.save()

    else:
        os.system('echo "The file is not yet done"')

        threading.Timer(TIME_TO_SEARCH, file_exists,args=(rmgpy,rmgdb, job, request)).start()
        threading.current_thread().cancel()