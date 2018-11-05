# code-exec-as-a-service
RESTful web service for running code snippets

# How to use

You should first check which languages are available with the `GET /` endpoint.
The you submit the base64 encoded source code for your selected language along with optional input strings.
The program should read only one input from stdin at the time and exit when it has processed one input. Input is sent to the program similar to this:
```bash
for input in inputs; then
    printf $input | /path/to/program
done
```

## Adding support for new languages
See [languages/README.md](languages/README.md)

## API endpoints

### GET /
Returns a list of available languages.
Example response (200):
```json
["C", "python", "node"]
```

### POST /exec/{language}
Post source code and (optinally) input to be sent to the process stdin.
The source code must be base64 encoded.
Example request to `/exec/C` :
```json
{
	"source": "I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxzdHJpbmcuaD4KCmludCBtYWluKHZvaWQpCnsKICAgIGNoYXIgYnVmWzEwMjRdOwoKICAgIG1lbXNldChidWYsIDAsIHNpemVvZihidWYpKTsKICAgIGZnZXRzKGJ1Ziwgc2l6ZW9mKGJ1ZiksIHN0ZGluKTsKCXByaW50ZigiSGVsbG8gd29ybGQsICVzXG4iLCBidWYpOwoKCXJldHVybiAwOwp9Cg==",
	"inputs": ["hi\n", "man\n"]
}
```
Response (http 200):
```json
[
	{
		"input": "hi\n",
		"output": {
			"status": "OK",
			"message": "Successfully executed code",
			"output": "Hello world, hi\n\n"
		}
	},
	{
		"input": "man\n",
		"output": {
			"status": "OK",
			"message": "Successfully executed code",
			"output": "Hello world, man\n\n"
		}
	}
]
```

If the code fails to build a http 400 and a json-message with `"status"` = `"BUILD_ERROR"` will be returned:
```json
{
	"status": "BUILD_ERROR",
	"message": "There was a build error",
	"output": "code.c: In function 'main':\ncode.c:12:10: error: expected ';' before '}' token\n  return 0\n          ^\n          ;\n }\n ~         \n"
}
```
