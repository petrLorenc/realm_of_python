This was used to set the "stage".

```shell
 ➜ cd version_a
 ➜ uv init --no-managed-python --bare    
Initialized project `version-a`

 ➜ uv init --no-managed-python --library my_library_database
Adding `my-library-database` as member of workspace `/Users/lorencp/PycharmProjects/apex-uv-playground/workspace_playground/version_a`
Initialized project `my-library-database` at `/Users/lorencp/PycharmProjects/apex-uv-playground/workspace_playground/version_a/my_library_database`

 ➜ uv init --no-managed-python --library my_library_genai   
Adding `my-library-genai` as member of workspace `/Users/lorencp/PycharmProjects/apex-uv-playground/workspace_playground/version_a`
Initialized project `my-library-genai` at `/Users/lorencp/PycharmProjects/apex-uv-playground/workspace_playground/version_a/my_library_genai`
 
 ➜ uv init --no-managed-python --application my_application  
Adding `my-application` as member of workspace `/Users/lorencp/PycharmProjects/apex-uv-playground/workspace_playground/version_a`
Initialized project `my-application` at `/Users/lorencp/PycharmProjects/apex-uv-playground/workspace_playground/version_a/my_application`
  
 ➜ cd my_library_database 
 ➜ uv add postgres  
 ➜ cd .. 
 
 ➜ cd my_library_genai 
 ➜ uv add openai  
 ➜ cd .. 
 
 ➜ cd my_application   
 ➜ uv add my_library_database            
 ➜ uv add my_library_genai   
 
 # update common.py in each library, and copy-paste versions (with removing some parts).
```