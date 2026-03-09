# Convenience functions for Ignition development, typically loaded
# as "shared.later" in v7.x.
#
# Copyright 2008-2019 Automation Professionals, LLC <sales@automation-pros.com>
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#   3. The name of the author may not be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

# Java 8 or later is required, due to the use of CompletableFuture and BiConsumer.

from java.lang import Runnable, StackTraceElement, Thread, Throwable
from java.util.concurrent import CompletableFuture
from java.util.function import BiConsumer

import java.lang.Exception
import sys

logger = system.util.getLogger("shared."+__name__)

#------------
# Handle gateway scope where invokeLater doesn't exist.
#
# Generic user code should use shared.later.invokeLater() instead of
# system.util.invokeLater() if gateway scope compatibility is needed.
#
try:
	invokeLater = system.util.invokeLater
except AttributeError:
	try:
		from com.inductiveautomation.ignition.gateway import IgnitionGateway as GwContext
	except:
		from com.inductiveautomation.ignition.gateway import SRContext as GwContext
	g = system.util.getGlobals()
	_old = g.get('FakeUIThreadExec', None)
	if _old:
		_old.shutdown()
	del _old
	_executor = GwContext.get().createExecutionManager('FakeUIThread', 1)
	g['FakeUIThreadExec'] = _executor
	class _runnable(Runnable):
		def __init__(self, func):
			self.func = func
		def run(self):
			self.func()

	def invokeLater(func, delay=0):
		delay = int(delay)
		if delay>0:
			_executor.executeOnce(_runnable(func), delay)
		else:
			_executor.executeOnce(_runnable(func))

#------------
# Java wrapper for Jython exceptions to preserve the python
# stack trace.
#
class PythonAsJavaException(java.lang.Exception):

	@staticmethod
	def fullClassName(cls):
		if cls.__bases__:
			return fullClassName(cls.__bases__[0])+"."+cls.__name__
		return cls.__name__

	def __init__(self, pyexc, tb=None):
		super(PythonAsJavaException, self).__init__(str(pyexc), None, True, True)
		traceElements = []
		if tb is None:
			tb = sys.exc_info()[2]
		while tb:
			code = tb.tb_frame.f_code
			vnames = code.co_varnames
			if vnames and vnames[0] in ('cls', 'self'):
				ref = tb.tb_frame.f_locals[vnames[0]]
				if vnames[0] == 'self':
					className = fullClassName(ref.__class__)
				else:
					className = fullClassName(ref)
			else:
				className = '<global>'
			traceElements.append(StackTraceElement(className, code.co_name, code.co_filename, tb.tb_lineno))
			tb = tb.tb_next
		self.setStackTrace(traceElements)

#------------
# Given a future, wait for it to complete, and log any exception produced
# at the warning level.  Return the given value if present, otherwise
# return the future's result.  This function must not be called on the GUI
# thread -- that will freeze the UI until the future completes.
#
def futureExLog(f, retv=None):
	try:
		if retv is None:
			retv = f.get()
		else:
			f.get()
	except java.lang.Exception, e:
		logger.warn("Future Exception:", e)
	return retv

#------------
# If a future needs only to have its exceptions logged, attach an instance
# of FutureLogger to it with .whenComplete().
#
# Like so:
#    shared.later.callAsync(.....).whenComplete(shared.later.FutureLogger())
#
class FutureLogger(BiConsumer):
	def accept(self, retv, exc):
		if exc:
			logger.warn("Future Exception:", exc)

#------------
# Asynchronous method execution
#
# This routine accepts a target function, and a variable argument list, and
# schedules the function call for asynchronous execution.  The function can
# be a bare (no parens) object method, but must not call any gui or
# gui component methods.
#
# The return value of the function completes a future, which is itself returned
# to caller.  If the caller discards the future, the target function's return
# value or exception will be discarded.
#
# Do *NOT* wait for the future in a GUI thread!
#
def callAsync(func, *args, **kwargs):
	future = CompletableFuture()
	def callAsyncInvoked():
		try:
			future.complete(func(*args, **kwargs))
		except Throwable, t:
			future.completeExceptionally(t)
		except Exception, e:
			future.completeExceptionally(PythonAsJavaException(e))
	system.util.invokeAsynchronous(callAsyncInvoked)
	return future

#------------
# Java Runnable wrapper for Python Callable with args
class JavaCallable(Runnable):
	__slots__ = ['_f', '_func', '_args', '_kwa']
	def __init__(self, future, func, *args, **kwargs):
		self._f = future
		self._func = func
		self._args = args
		self._kwa = kwargs
	def run(self):
		try:
			self._f.complete(self._func(*self._args, **self._kwa))
		except Throwable, t:
			self._f.completeExceptionally(t)
		except Exception, e:
			self._f.completeExceptionally(PythonAsJavaException(e))

#------------
# Asynchronous method execution
#
# This routine accepts a target function, a thread name, and a variable
# argument list, and schedules the function call for asynchronous execution
# in a java Thread of that name.  The function can
# be a bare (no parens) object method, but must not call any gui or
# gui component methods.
#
# The return value of the function completes a future, which is itself returned
# to caller (along with the thread itself).  If the caller discards the future,
# the target function's return value or exception will be discarded.
#
# Do *NOT* wait for the future in a GUI thread!
#
def callThread(func, threadName, *args, **kwargs):
	future = CompletableFuture()
	runnable = JavaCallable(future, func, *args, **kwargs)
	thread = Thread(runnable, threadName)
	thread.start()
	return (future, thread)

#------------
# Deferred property assignment
#
# Procedures executing in the 'invokeAsynchronous' environment are not allowed
# to assign to properties of gui objects.  This routine accepts a target
# object, a property name, and a new value, and schedules the assignment
# in the gui thread.
#
# Successful assignment completes a future with a None value.  The future is
# returned to the caller.  If the caller discards the future, the target
# assignment's success or failure will be discarded.
#
# Do *NOT* wait for the future in a GUI thread!
#
# An emulation of invokeLater is used in gateway scopes.
#
def assignLater(comp, prop, val, ms = 0):
	future = CompletableFuture()
	def assignLaterInvoked():
		try:
			try:
				setattr(comp, prop, val)
			except AttributeError:
				comp.setPropertyValue(prop, val)
			future.complete(None)
		except Throwable, t:
			future.completeExceptionally(t)
		except Exception, e:
			future.completeExceptionally(PythonAsJavaException(e))
	invokeLater(assignLaterInvoked, ms)
	return future

#------------
# Deferred property assignment from a background function
#
# Functions executing in the 'invokeAsynchronous' environment are not allowed
# to assign to properties of gui objects.  This routine accepts a target
# object, a property name, a callable function, and its arguments, runs the
# function in the background, then schedules the assignment of the result
# in the gui thread.
#
# Successful assignment completes a future with a None value.  The future is
# returned to the caller.  If the caller discards the future, the target
# assignment's success or failure will be discarded.
#
# Do *NOT* wait for the future in a GUI thread!
#
# An emulation of invokeLater is used in gateway scopes, though somewhat
# pointless, as there are no gui objects in the gateway.  But it works on
# any arbitrary object's properties.
#
def assignAsyncLater(comp, prop, func, *args, **kwargs):
	future = CompletableFuture()
	def assignAsyncLaterInvoked():
		try:
			val = func(*args, **kwargs)
			def assignLaterInvoked():
				try:
					try:
						setattr(comp, prop, val)
					except AttributeError:
						comp.setPropertyValue(prop, val)
				except Throwable, t:
					future.completeExceptionally(t)
				except Exception, e:
					future.completeExceptionally(PythonAsJavaException(e))
				future.complete(val)
			invokeLater(assignLaterInvoked)
		except Throwable, t:
			future.completeExceptionally(t)
		except Exception, e:
			future.completeExceptionally(PythonAsJavaException(e))
	system.util.invokeAsynchronous(assignAsyncLaterInvoked)
	return future

#------------
# Deferred method execution
#
# Procedures executing in the 'invokeAsynchronous' environment are not allowed
# to execute methods of gui objects.  This routine accepts a target
# function, and a variable argument list, and schedules the function call
# in the gui thread.  The function can be a bare (no parens) object method.
#
# The return value of the function completes a future, which is itself returned
# to caller.  If the caller discards the future, the target function's return
# value or exception will be discarded.
#
# Do *NOT* wait for the future in a GUI thread!
#
# An emulation of invokeLater is used in gateway scopes.
#
def callLater(func, *args, **kwargs):
	future = CompletableFuture()
	def callLaterInvoked():
		try:
			future.complete(func(*args, **kwargs))
		except Throwable, t:
			future.completeExceptionally(t)
		except Exception, e:
			future.completeExceptionally(PythonAsJavaException(e))
	invokeLater(callLaterInvoked)
	return future

#------------
# Deferred Asynchronous method execution
#
# This routine accepts a target function, and a variable argument list, and
# schedules the function call for asynchronous execution, but only after also
# waiting for gui events to complete.  The function can be a bare (no parens)
# object method, but must not call any gui or gui component methods.
#
# The return value of the function completes a future, which is itself returned
# to caller.  If the caller discards the future, the target function's return
# value or exception will be discarded.
#
# Do *NOT* wait for the future in a GUI thread!
#
# An emulation of invokeLater is used in gateway scopes.
#
def callAsyncLater(func, *args, **kwargs):
	future = CompletableFuture()
	def callLaterInvoked():
		def callAsyncInvoked():
			try:
				future.complete(func(*args, **kwargs))
			except Throwable, t:
				future.completeExceptionally(t)
			except Exception, e:
				future.completeExceptionally(PythonAsJavaException(e))
		system.util.invokeAsynchronous(callAsyncInvoked)
	invokeLater(callLaterInvoked)
	return future

#------------
# Deferred Asynchronous method execution
#
# This routine accepts a target function, a time, and a variable argument
# list, and schedules the function call for asynchronous execution, but
# only after also waiting the specified milliseconds after all gui events
# complete.  The function can be a bare (no parens) object method, but must
# not call any gui or gui component methods.
#
# The return value of the function completes a future, which is itself returned
# to caller.  If the caller discards the future, the target function's return
# value or exception will be discarded.
#
# Do *NOT* wait for the future in a GUI thread!
#
# An emulation of invokeLater is used in gateway scopes.
#
def callAsyncDelayed(func, delay=1000, *args, **kwargs):
	future = CompletableFuture()
	def callLaterInvoked():
		def callAsyncInvoked():
			try:
				future.complete(func(*args, **kwargs))
			except Throwable, t:
				future.completeExceptionally(t)
			except Exception, e:
				future.completeExceptionally(PythonAsJavaException(e))
		system.util.invokeAsynchronous(callAsyncInvoked)
	invokeLater(callLaterInvoked, delay)
	return future

#------------
# Deferred tag assignment
#
# This routine accepts a target tag path and a new value, and
# schedules the assignment in the gui thread.
def writeTagLater(tag, val, ms = 0):
	def writeTagLaterInvoked():
		system.tag.write(tag, val, True)
	invokeLater(writeTagLaterInvoked, ms)
	return val

#------------
# Deferred tag assignment
#
# This routine accepts a list of target tag paths and corresponding list of
# new values, and schedules the assignment in the gui thread.
def writeTagsLater(taglist, vallist, ms = 0):
	future = CompletableFuture()
	def writeTagsLaterInvoked():
		system.tag.writeAll(taglist, vallist)
	invokeLater(writeTagsLaterInvoked, ms)

#------------
# Deferred tag assignment
#
# This routine accepts a list of target tag paths and corresponding list of
# new values, and schedules the assignment synchronously in a background
# thread.  Then a property assignment is scheduled back on the gui thread.
def writeAsyncAssign(taglist, vallist, comp, prop, val):
	def writeAsyncAssignInvoked():
		for t, v in map(None, taglist, vallist):
			system.tag.writeSynchronous(t, v, 250)
		app.util.assignLater(comp, prop, val)
	system.util.invokeAsynchronous(writeAsyncAssignInvoked)

