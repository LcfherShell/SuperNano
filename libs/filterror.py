import re, os, sys, compileall, collections, traceback
try:
    import gc
except:
    pass
from contextlib import contextmanager

class Decoration:
    def __init__(self, param_foo='a', param_bar='b'):
        self.param_foo = param_foo
        self.param_bar = param_bar

    def __call__(self, func):
        def my_logic(*args, **kwargs):
            print(self.param_bar)
            # including the call to the decorated function (if you want to do that)
            result = func(*args, **kwargs)
            return result

        return my_logic

class PYTHON_ERORCODE:
    all_error = collections.OrderedDict()
    all_error[Exception] = Exception
    all_error[TypeError] = TypeError
    all_error[TimeoutError] = TimeoutError
    all_error[RecursionError] = RecursionError
    all_error[ReferenceError] = RecursionError
    all_error[MemoryError] = MemoryError
    all_error[ModuleNotFoundError] = ModuleNotFoundError
    all_error[ChildProcessError] = ChildProcessError
    all_error[ConnectionAbortedError] = ConnectionAbortedError
    all_error[ConnectionError] = ConnectionError
    all_error[ConnectionRefusedError] = ConnectionRefusedError
    all_error[ConnectionResetError] = ConnectionResetError
    all_error[OSError] = OSError
    all_error[OverflowError] = OverflowError
    all_error[EnvironmentError] =EnvironmentError
    all_error[EOFError] = EOFError
    all_error[UnicodeDecodeError] = UnicodeDecodeError
    all_error[UnicodeEncodeError] = UnicodeEncodeError
    all_error[UnicodeTranslateError] = UnicodeTranslateError
    all_error[UnboundLocalError] = UnboundLocalError
    all_error[AttributeError] = AttributeError
    all_error[ValueError] = ValueError
    all_error[AssertionError] =AssertionError
    all_error[ZeroDivisionError] = ZeroDivisionError
    all_error[FloatingPointError] = FloatingPointError
    all_error[FileNotFoundError] =FileNotFoundError
    all_error[FileExistsError] = FileExistsError
    all_error[KeyboardInterrupt] = KeyboardInterrupt
    all_error[NameError] = NameError


class ValidationError(PYTHON_ERORCODE):
    global __clasesserr
    def __init__(self, coderror=None, messages=None):
        
        global messages_error
        
        messages_error= messages
        __, __clasesserr = None, None
        
        if coderror in self.all_error and messages:
            try:
                for keys in self.all_error.keys():
                    if coderror == str(keys):
                        coderror = str(self.all_error[keys])
                        break
                    else:
                        code = self.all_error[keys]
                        if str(keys).count(".") != 0:
                            newkeys = re.findall(r"'(.*?)'", str(keys).strip()) or re.findall(r"\"(.*?)\"", str(keys).strip())
                            if newkeys.__len__()!=0:
                                newkeys  = newkeys[-1:][0]
                                assert str(newkeys) == code
                                coderror = str(newkeys)
                                break
                if coderror.startswith("<class"):
                    newkeys  = re.findall(r"'(.*?)'", str(coderror).strip()) or re.findall(r"\"(.*?)\"", str(coderror).strip())
                    coderror = str(newkeys[-1:][0]).split(".")[-1:][0]

            except:
                codex = str(coderror).strip()
                newkeys = re.findall(r"'(.*?)'", str(codex).strip()) or re.findall(r"\"(.*?)\"", str(codex).strip())
                if newkeys.__len__() != 0:
                    codex = newkeys[-1:][0]
                    coderror = codex
                    
                        
            try:
                __ = eval("{coderrorx}(\"{messages}\")".format(coderrorx=coderror, messages=str(messages)))
                
            except:
                
                __ = "\"{messages}\"".format(messages=str(messages))
            finally:
                __clasesserr = "{coderrorx}".format(coderrorx=str(coderror))
            


        else:
        
            regex = []
        
            for keys in self.all_error.keys():
        
                if coderror == str(keys):
        
                    regex = re.findall(r"'(.*?)'", str(keys).strip()) or re.findall(r"\"(.*?)\"", str(keys).strip())
                    break
                else:
                    try:
                        code = self.all_error[keys]
                        if keys.count(".") != 0:
                            newkeys = re.findall(r"'(.*?)'", str(keys).strip()) or re.findall(r"\"(.*?)\"", str(keys).strip())
                            if newkeys.__len__()!=0:
                                newkeys  = newkeys[-1:][0]
                                assert str(newkeys) == code
                                regex = [newkeys]
                                break
                    except:
                        pass
            
        
            if regex.__len__() > 0:
        
                try:
        
                    __ = eval("{coderrorx}(\"{messages}\")".format(coderrorx=regex[-1:][0], messages=str(messages)))
        
                except:
        
                    __ = "\"{messages}\"".format(messages=str(messages))
                
                finally:
                    __clasesserr = "{coderrorx}".format(coderrorx=regex[-1:][0])
            
                
                #return __
        self.compliterror = __
        self.classeseror = __clasesserr
        if self.compliterror == None:
            messages_error = str(messages)
    
    def __call__(self, coderror=None, messages=None):
        global messages_error
        
        messages_error= messages
        __, __clasesserr = None, None
        
        if coderror in self.all_error and messages:

            for keys in self.all_error.keys():
                if coderror == str(keys):
                    coderror = self.all_error[keys]
                    break
                else:
                    code = self.all_error[keys]
                    if keys.count(".") != 0:
                        newkeys = re.findall(r"'(.*?)'", str(keys).strip()) or re.findall(r"\"(.*?)\"", str(keys).strip())
                        if newkeys.__len__()!=0:
                            newkeys  = newkeys[-1:][0]
                            assert str(newkeys) == code
                            coderror = newkeys
                            break
                        
            try:
                __ = eval("{coderrorx}(\"{messages}\")".format(coderrorx=coderror, messages=str(messages)))
                
            except:
                
                __ = "\"{messages}\"".format(messages=str(messages))
            finally:
                __clasesserr = "{coderrorx}".format(coderrorx=str(coderror))
            


        else:
        
            regex = []
        
            for keys in self.all_error.keys():
        
                if coderror == str(keys):
        
                    regex = re.findall(r"'(.*?)'", str(keys).strip()) or re.findall(r"\"(.*?)\"", str(keys).strip())
                    break
                else:
                    try:
                        code = self.all_error[keys]
                        if keys.count(".") != 0:
                            newkeys = re.findall(r"'(.*?)'", str(keys).strip()) or re.findall(r"\"(.*?)\"", str(keys).strip())
                            if newkeys.__len__()!=0:
                                newkeys  = newkeys[-1:][0]
                                assert str(newkeys) == code
                                regex = [newkeys]
                                break
                    except:
                        pass
        
            if regex.__len__() > 0:
        
                try:
        
                    __ = eval("{coderrorx}(\"{messages}\")".format(coderrorx=regex[-1:][0], messages=str(messages)))
        
                except:
        
                    __ = "\"{messages}\"".format(messages=str(messages))
                
                finally:
                    __clasesserr = "{coderrorx}".format(coderrorx=regex[-1:][0])
            
                
                #return __
        exc_type, exc_obj, exc_tb = sys.exc_info()

        typess = str(exc_type).split(".")[-1:][0].replace("'>", "", 1).strip()
        self.compliterror = __
        self.classeseror = __clasesserr
        if self.classeseror == None or self.classeseror == "" or self.classeseror == "None":
            if coderror == None:
                coderror = "<class 'filterror._'>"
            coderrorx = re.findall(r"'(.*?)'", str(coderror).strip()) or re.findall(r"\"(.*?)\"", str(coderror).strip())
            for keys in self.all_error.keys():
                    try:
                        splikeys = re.findall(r"'(.*?)'", str(self.all_error[keys]).strip()) or re.findall(r"\"(.*?)\"", str(self.all_error[keys]).strip())
        
                    except:
                        splikeys = re.findall(r"'(.*?)'", str(keys).strip()) or re.findall(r"\"(.*?)\"", str(keys).strip())

                    newkeys = str(splikeys[-1:][0]).split(".")[-1:][0]
                    if newkeys == str(coderrorx[-1:][0]).split(".")[-1:][0] and newkeys == typess:
                        self.classeseror = keys
                        break
                    elif newkeys == str(coderrorx[-1:][0]).split(".")[-1:][0]:
                        self.classeseror = keys
                        break
                    elif coderror == "<class 'filterror._'>" and newkeys == typess or coderror == "_" and newkeys == typess:
                        self.classeseror = keys
                        break
            if self.compliterror == None or self.compliterror == "":
                if messages == None:
                    self.compliterror = str(exc_obj)
                    messages_error = self.compliterror
                else:
                    self.compliterror = str(messages)
                    
        
        return self

    def __enter__(self):
        return self
    

    def __str__(self):
        return ""

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        return self.__dict__

    def __dir__(self):
        return ['results']
    
    def update(self, run:bool, **kwarg:dict):
        if kwarg.__len__() != 0:
            for x in kwarg.keys():

                keys, values = x, kwarg[x]
                if keys:

                    valuesx = """class {classname}(Exception):\n\tpass""".format(classname=keys)
                        
                    exec(valuesx)
                    self.all_error[eval(keys)] = eval(keys)
                    #setattr(__builtins__, "{classname}".format(classname=values), eval(keys))

                else:
                    if isinstance(values, str):
                        
                        if values.find(".") != 0 and values.find(".") > 0:
                            
                            values = values.split(".")[-1:][0]

                        
                        elif values.startswith("."):
                           
                            if values.count(".") > 0:
                           
                                values = values.split(".")[-1:][0]
                           
                            else:
                           
                                values = values.replace(".", "", 1)
                        
                        valuesx = """
                        class {classname}(Exception):

                            def __init__(self, code):
                                self.code = code

                            def __str__(self):
                                return repr(self.code)

                        """.format(classname=values)
                        
                        exec(valuesx)
                        self.all_error[eval(values)] = eval(values)
                        #setattr(__builtins__, "{classname}".format(classname=values), eval(values))

                    elif isinstance(values,object):
                        self.all_error[eval(values)] = eval(values)
                        #setattr(__builtins__, "{classname}".format(classname=values), eval(values))
                    else:
                        pass
                    
        #print(valuesx)
        #try:
        #    @Decoration(param_bar=self)
        #    def example():
        #        return self
        #    return example()
        #except:
        #    return self.__init__(coderror=values)

    @property
    def results(self):
        
        if self.__dict__.keys().__contains__("jsonoutput"):
        
            json = self.jsonoutput
        
            self.jsonoutput = collections.OrderedDict()
        

        return json
    

    def manual(self):
        
        self.jsonoutput = collections.OrderedDict()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        try:
            class A(eval(self.classeseror)):
            
                def __init__(self, code):
                    self.code = code
                
                def __str__(self):
                    return repr(self.code)
        except:
            try:
                class A(self.classeseror):

                    def __init__(self, code):
                        self.code = code
                    
                    def __str__(self):
                        return repr(self.code)
            except:
                self.jsonoutput['Type_Error'], self.jsonoutput['pathname'], self.jsonoutput["filename"]\
                , self.jsonoutput['error_line'], self.jsonoutput['error_message'] = None, None, None, None, None
                pname, fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)
                if fname == "<stdin>":
                    try:
                        fname = os.chdir()
                    except:
                        fname = "."

                #if exc_type not in self.all_error:
                exc_typeinject = re.findall(r"'(.*?)'", str(exc_type).strip()) or re.findall(r"\"(.*?)\"", str(exc_type).strip())
                exc_typeinject = ".".join(["filterror", str(exc_typeinject[-1:][0].split(".")[-1:][0]) ])
                for keys in self.all_error.keys():
                        newkeys = str(keys)
                        if newkeys.find(exc_typeinject) != 0 or newkeys.find(exc_type) != 0:
                            self.jsonoutput['Type_Error'] = newkeys.split(".")[-1:][0]
                            self.jsonoutput['pathname'] = pname
                            self.jsonoutput["filename"] = fname
                            self.jsonoutput['error_line'] = exc_tb.tb_lineno
                            self.jsonoutput['error_message'] =  str(exc_obj)
                            break
                error_type = re.findall(r"'(.*?)'",  str(self.jsonoutput['Type_Error']).strip()) or re.findall(r"\"(.*?)\"",  str(self.jsonoutput['Type_Error']).strip())
                if error_type.__len__() == 0:

                    error_type = str(self.jsonoutput['Type_Error'])
                
                else:
                
                    error_type = str(error_type[-1:][0]).split(".")[-1:][0]
                self.jsonoutput.update({"Type_Error": error_type})
                return 
        
        messages = str(self.compliterror)
        
        if messages.startswith(str(self.classeseror)):
        
            messages  = messages.replace(str(self.classeseror), "", 1)
        
        try:
        
            try:
        
                raise A(messages)
        
            finally:
        
                raise A(messages)
        
        except A as output:
            #print("Type Error:", self.classeseror)
            error_type = re.findall(r"'(.*?)'",  str(self.classeseror).strip()) or re.findall(r"\"(.*?)\"",  str(self.classeseror).strip())
            if error_type.__len__() == 0:

                error_type = str(self.classeseror)
            
            else:
            
                error_type = str(error_type[-1:][0]).split(".")[-1:][0]
                
            #exc_type, exc_obj, exc_tb = sys.exc_info()
            roscz = [e for e in str(output).split("\n") if e.__len__()!=0]
            
            check_filename, lines_X, code_messages = [], "", ""
            
            if messages_error != "None" or messages_error != None:
                __ = traceback.format_exception(exc_type, exc_obj, exc_tb)
                code_messages = str(__[-1:][0]).replace("ValidationError.manual.<locals>.A:", "", 1).strip()
            else:
                code_messages = str(exc_obj)
                
                

            for index_output in roscz:
                
                if str(index_output).strip().startswith(("File \"", "File: \"", "file \"")):

                    cleanx = str(index_output).strip().rstrip()
                
                    check_filename = re.findall(r"'(.*?)'", cleanx) \
                        or re.findall(r"\"(.*?)\"", cleanx)
                
                    lines_X = cleanx
            else:
                if check_filename.__len__() == 0:
                    check_filename = []
            
            if check_filename.__len__() != 0:
                
                pname, fname = os.path.split(check_filename[-1:][0].strip())
                
                linex = re.findall(r"line\s+(.*),", lines_X) or re.findall(r"line\s+(.*,)", lines_X)
                if linex:
                    linerror = int(linex[-1:][0])
                    #errotypes = roscz[-1:][0]
                    self.jsonoutput['Type_Error'] = error_type
                    
                    self.jsonoutput['pathname'] = pname
                    
                    self.jsonoutput["filename"] = fname
                    
                    self.jsonoutput['error_line'] = linerror
                else:
                    self.jsonoutput['error_message'] = code_messages
            else:
                self.jsonoutput['Type_Error'] = error_type
                if str(output).find("File"):
                    roscz = [e.strip() for e in str(output).split("\n") if e.__len__()!=0]
                    
                    check_filename, lines_X = [], ""
                    
                    for xfile in roscz:
                    
                        if xfile.startswith(("File", "file")):
                            cleanx = str(xfile).strip().rstrip()
                    
                            check_filename = re.findall(r"'(.*?)'", cleanx) \
                                or re.findall(r"\"(.*?)\"", cleanx)
                    
                            lines_X = cleanx
                    
                    if check_filename.__len__():
                        
                        linex = re.findall(r"line\s+(.*),", lines_X) or re.findall(r"line\s+(.*,)", lines_X)
                        
                        linerror = (linex[-1:][0])
                        #errotypes = roscz[-1:][0]
                        pname, fname = os.path.split(check_filename[-1:][0].strip())
                    
                        self.jsonoutput['Type_Error'] = error_type
                    
                        self.jsonoutput['pathname'] = pname
                    
                        self.jsonoutput["filename"] = fname
                    
                        self.jsonoutput['error_line'] = linerror
                    
                    else:
                        self.jsonoutput['error_message'] = code_messages

                    #self.jsonoutput['error_message'] = str(output)
                else:
                    self.jsonoutput['error_message'] = code_messages

            
            if self.jsonoutput.get('filename') == "<stdin>":
                del self.jsonoutput['filename']
                try:
                    self.jsonoutput['pathname'] = os.chdir()
                except:
                    self.jsonoutput['pathname'] = "."
            
        if self.jsonoutput.get('error_message'):
                exc_type, exc_obj, exc_tb = sys.exc_info()
                try:
                    _modules = os.path.abspath(str(sys.modules['__main__'].__file__ ))
                    pname, fname = os.path.split(str(__file__).strip())
                    self.jsonoutput['pathname'] = pname
                    self.jsonoutput["filename"] = fname
                    
                except:
                    self.jsonoutput['pathname'] = "."
                
                #messages = self.jsonoutput["error_message"]
                self.jsonoutput['error_line'] = exc_tb.tb_lineno
                del self.jsonoutput["error_message"]
                self.jsonoutput['error_message'] = code_messages

        else:
                self.jsonoutput['error_line'] = exc_tb.tb_lineno
                self.jsonoutput['error_message'] = code_messages

        self.compliterror = None
            
        self.classeseror = None

        regex = re.findall(r"'(.*?)'", str(error_type).strip()) or re.findall(r"\"(.*?)\"", str(error_type).strip())
        if regex.__len__() != 0:
            self.jsonoutput['Type_Error'].update({'Type_Error': regex[-1:][0] })
                #self.jsonoutput['error_line'] = linex
                    #regex = re.findall(r"'(.*?)'", str(errotypes).strip()) or re.findall(r"\"(.*?)\"", str(errotypes).strip())


            #exc_type, exc_obj, exc_tb = sys.exc_info()
            #pname, fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)
            #print("EROR2 ", exc_type, fname, exc_tb.tb_lineno)
            #print(tb)
    
    def auto(self):

        """
        
        
        
        """
        exc_type, exc_obj, exc_tb = sys.exc_info()
        
        pname, fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)
        
        typeserror = re.findall(r"'(.*?)'", str(exc_type).strip()) \
            or re.findall(r"\"(.*?)\"", str(exc_type).strip())
        
        self.jsonoutput = collections.OrderedDict()
        
        self.jsonoutput['Type_Error'] = typeserror[-1:][0]
        
        self.jsonoutput['pathname'] = pname
        
        self.jsonoutput["filename"] = fname
        
        self.jsonoutput['error_line'] = exc_tb.tb_lineno

        if self.jsonoutput.get('filename') == "<stdin>":
            del self.jsonoutput['filename']
            try:
                self.jsonoutput['pathname'] = os.chdir()
            except:
                self.jsonoutput['pathname'] = "."
                
        self.jsonoutput['error_message'] = str(exc_obj)

    def capture(self, types=2, *args):
        if types == 2 or types == 1:
            def foo(exctype, value, tb):
                trace_back = traceback.extract_tb(tb)
                stack_trace = []
                for trace in trace_back:
                    stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
                print('My Error Information')
                print('Type:', exctype)
                print('Value:', value)
                print('Traceback:', "\n".join(stack_trace))

            sys.excepthook = foo
        else:
            def handle_exception(exc_type, exc_value, exc_traceback):
                if issubclass(exc_type, KeyboardInterrupt):
                    sys.__excepthook__(exc_type, exc_value, exc_traceback)
                    return
                #logging.critical(exc_value, exc_info=(exc_type, exc_value, exc_traceback))


            def handle_error(func):
                def __inner(*args, **kwargs):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        stack_trace = []
                        exc_type, exc_value, exc_tb = sys.exc_info()
                        trace_back = traceback.extract_tb(exc_tb)
                        for trace in trace_back:
                            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
                        handle_exception(exc_type, exc_value, exc_tb)
                        print('My Error Information')
                        print('Type:', exc_type)
                        print('Value:', exc_value)
                        print('Traceback:', "\n".join(stack_trace))

                return __inner
            return handle_error

example = """Traceback (most recent call last):
File "C:/Users/pc/Documents/WindowsPowerShell/libs/filterror.py", line 136, in <module>
import sdd
ModuleNotFoundError: No module named 'sdd'
"""



"""""try:
    myfunc()
except:
    type, val, tb = sys.exc_info()
    #print(sys.exc_info())
    traceback.clear_frames(tb)
# some cleanup code
gc.collect()
# and then use the tb:
if tb:
    print("EROR2 :", val, type, tb)

import sys, os

"""""
#simple_test =  ValidationError("<class 'Exception'>", example)

#Simple
#simple_test.capture()
#simple_test.manual()
#print(simple_test.results)
#sgsgs()

#try:
#    gsgs()
#except Exception as e:
#    with ValidationError() as simple_test:
#        simple_test.auto()
#        print(simple_test.results)

#try:
#    gsgs()
#except Exception as e:
#    with ValidationError("<class 'Exception'>", messages=e) as simple_test:
#        simple_test.manual()
#        print(simple_test.results)
        
        #print("\nDete:", simple_test.__dict__)



#@simple_test.capture(1)
#def main():
#    raise RuntimeError("RuntimeError")


#if __name__ == "__main__":
#    for _ in range(1, 20):
#        main()
__all__ = ['PYTHON_ERORCODE', 'ValidationError']