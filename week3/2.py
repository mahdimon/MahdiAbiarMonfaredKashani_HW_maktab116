import os
def sed(file_input,file_output,replacement_string,pattern_string):
    arguements = locals().items()
    errors = {"TypeError":[] , "FileNotFoundError":[], "PermissionError":[] , "anythingelse":[]}
    
    for name,value in arguements:
         
        if not isinstance(value,str):
            errors["TypeError"].append(f"{name} must be str you imported {value}")
       

        elif name == "file_input":
            try:
                file_input = open(file_input)
            except FileNotFoundError:
                errors["FileNotFoundError"].append(f"this file cannot be found: file_input = {value}")
            except PermissionError:
                errors["PermissionError"].append(f"you dont have permition to read this file: file_input = {value}")
            except Exception as e:
                errors["anythingelse"].append(f'somthing went wrong in oppening file_input: {value}\n{e}')
            
        elif name == "file_output":
            try:
                output_path = file_output
                file_output = open(file_output,"w")
                    
            except PermissionError:
                errors["PermissionError"].append(f"you dont have permition to write this file: file_output = {value}")
            except Exception as e:
                errors["anythingelse"].append(f'somthing went wrong in oppening file_output: {value}\n{e}')
    error = False
    for value in errors.values():
        if len(value) > 0:
            error = True
            for i in value:
                print(i)
    
    if error == True:
        if not isinstance(file_input,str):
            file_input.close()
        if not isinstance(file_output,str): 
            file_output.close()
            os.remove(output_path)
        print("function terminated")
        return False
    
    else:
        try:
            txt = file_input.read()
        except UnicodeError:
            raise UnicodeError("file has uncompatible characters")
        except IOError as e:
            raise IOError("something went wrong while reading the file"+str(e))
        except Exception as e:
            raise Exception(str(e))
        finally:
            file_input.close()
        
        txt = txt.replace(pattern_string,replacement_string)
        
        try:
            file_output.write(txt)
        except Exception as e:
            raise Exception(e)
        finally:
            file_output.close()
        
                          
sed("4","3","s",3)          
#sed("2-file.txt","2-output","output","input")          