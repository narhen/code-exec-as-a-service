# How to add new a language
Use `C/` as a reference when adding new languages.

1. Create a new directory and give it the name of the language you are adding. This name will be the
   one to use when using the API to execute code with language.
2. Enter the new directory and create these three files:
    - **Dockerfile**: The docker file where you set up the environment and necessary dependencies.
      In addition to installing dependencies you need to add a new user called "user", and shell
      scripts for building and running code (`build_program.sh` and `run_program.sh`). Make sure to
      put them somewhere in `PATH`.
    - **build_program.sh**: This script will be invoked in order to build the code submitted by users.
      **The script will receive one parameter**, which is the path to the program being built.
      Files created during building should be created in the same directory as the source code.
      Finally, the script should print a json formatted string with a `status` field, and an
      `outfile` field. f.ex `{"status": "ok", "outfile": "executable_file"}` or
      `{"status": "error", "outfile": "build_error.txt"}`.
    - **run_program.sh**: This script will be invoked in order to run the compiled code submitted by users.
      **The script will receive one parameter**, which is the path to the program being executed.
      The script should print a json formatted string with a `status` field, and an
      `outfile` field. f.ex `{"status": "ok", "outfile": "program_output.txt"}`.
3. Build the docker image: `$ docker build -t lang:$(basename $PWD) .`
4. Check whether the output from `GET host:port/` contains the language you just added.
5. Verify that everything is working by running code in your language via the `POST /exec/{lang}`
   endpoint.
