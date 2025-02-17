# Service-Authentication

This service provide a lambda that closely mirrors Authentication in
Central-API. Other service with API-Gateways can import this lambda, and attach
it as Authorizer.

The Lambda was setup to specifically work API-GatewayV2 (HttpApi).

# Examples

## Import

In order for another service to utilize the lambda as an authorizer it must
first import it:

```typescript
  private importAuthorizerLambda(
    stage: StackStage, // eph-poc-int-stage-prod
    prefix?: string //used to make compatible with ephemeral environment deploys
  ): IFunction {
    const resourcePrefix = prefix ? `${prefix}-` : ""

    //the name of the lambda to import
    const resourceName = `${resourcePrefix}serviceauth-${stage}-strict-auth`

    //importing the function via its Arn. Assumes hub production account
    return PythonFunction.fromFunctionArn(
      this,
      `${Stack.of(this).stackName}-auth`,
      Arn.format({
        account: Stack.of(this).account,
        arnFormat: ArnFormat.COLON_RESOURCE_NAME,
        partition: "aws",
        region: Stack.of(this).region,
        resource: "function",
        resourceName: resourceName,
        service: "lambda",
      })
    )
  }
```

If attempting to import the lambda from an account other than the Hub Account,
ensure this repository is updated with the proper permissions.

## Attach To HttpApi

AWS CDK is still growing, as such not all resources have a Level2 Construct.
APIGatewayV2 or its HttpApi does not have a Level2 Construct in the base CDK
package. To utilize an HttpApi the following cdk packages will also need to be
added to a project:

- [@aws-cdk/aws-apigatewayv2-alpha](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-apigatewayv2-alpha-readme.html)
- [@aws-cdk/aws-apigatewayv2-authorizers-alpha](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-apigatewayv2-authorizers-alpha-readme.html)

After the modules are install prior to setting up the HttpApi but after
importing the Lambda create an HttpLambdaAuthorizerInstances:

```typescript
const authorizer = new HttpLambdaAuthorizer(
  "StrictAuthorizer",
  importedAuthorizerLambda,
  {
    authorizerName: `${Stack.of(this).stackName}-auth`,
    responseTypes: [HttpLambdaResponseType.SIMPLE], // must be set to Simple
    identitySource: ["$request.header.cookie"], // must be the cookie
  }
)
```

Create an instance of an HttpApi:

```typescript
new HttpApi(this, `${stackName}`, {
  apiName: "my-gateway-name",
  defaultAuthorizer: authorizer,
  corsPreflight: {
    allowHeaders: [
      "Authorization",
      "Content-Type",
      "X-Amz-Date",
      "X-Api-Key",
      "Cookie",
    ],
    allowMethods: [CorsHttpMethod.ANY],
    allowCredentials: false,
  },
})
```

# Developing

## Getting Started

To get started you will need Python 3.11 and `pipenv` installed.

At the root of the repository simply:

```shell
pipenv sync
```

Or alternatively:

```shell
pipenv install
pipenv install -d
```

## Recommended ~/.zshrc or ~/.bashrc, etc Changes

A common practice in developing Python projects is to setup a virtual
environment (`.venv` folder) at the root of a projects directory. The default
behavior of many package installers (`pipenv`, `poetry`, `etc`) is to create a
`.venv` folder elsewhere in the user directory.

To force `pipenv` create a `.venv` in a project's root add the following to
your systems:

```shell
export PIPENV_VENV_IN_PROJECT=1
```

## Package Management

This project uses `pipenv` in favor of [poetry](https://python-poetry.org/), but
it can be modified to use `poetry` with very little effort.

`pipenv`` was chosen over poetry for 2 simple reasons:

1. Has a bit more ease working with packages that may be stored in CodeArtifact
2. A bit easier to setup a `.venv` file within a project's root.

In a lot of other areas `poetry` is better.

## Formatting

This repository uses Prettier to format the TypeScript Infrastructure code and
utilizes [Black](https://github.com/psf/black) to format Python code in the
`app/` directory.

Most IDEs contain a plugin or utility for running `Black`, but it can also be
run from the command line via:

```shell
pipenv run python -m black {path_to_dir}
```

IE:

```shell
pipenv run python -m black app
```

More information about the formatter can be found
[here](https://black.readthedocs.io/en/stable/).

## Linting

Though Python is a ducked-type language types can be enforced (partially) via
a Linter, in this case [MyPy](https://mypy-lang.org/).

MyPy adds static type checking to python and has several typing package, plugins
to allow typing of other dependencies that may not provide their own typing.

One such typing dependency is the package
[boto3-stub](https://github.com/youtype/mypy_boto3_builder) which provides
typing to AWS's Python SDK: boto3. Not only do these stubs provide type hints
they provide documentation and examples.

Most Python IDEs contain a MyPy plugin or utility, but it can also be run from
a shell with the following command:

```shell
pipenv run python -m mypy {path_to_file}
```

IE:

```shell
pipenv run python -m mypy app/
```

## Dependencies

This template utilizes Lambda Layers for deployed code. When developing locally
all dependencies should be installed as a dev dependency.

This keeps the lambda dependencies small and reduces cold start, and execution
times.

To add a new dependency to Layer utilized by the lambdas:

1. Install the dependency as dev dependency at the root of the project:

```shell
piepnv install requests -d
```

2. Navigate to the `infrastructure/layers/python` directory and install the
   dependency here as well:

```shell
pipenv install requests
```

Depending on your IDE setup this may have to be done in a separate shell window.

3. Be sure to remove any `.venv` folders created in the
   `infrastructure/layers/python` during this process.

### Scripting

This repository contains a `scripts`` folder that can be used to create a CLI to
interact with a Deployed application in AWS.

It is setup to have access to any module withing the `app/src` directory,
allowing for the script to use the existing models, services, and resources of
the base application.

The base CLI utilizes [click](https://click.palletsprojects.com/en/8.1.x/)
along with [rich](https://github.com/Textualize/rich) to provide a base
template.

To run the CLI enter the following command:

```shell
pipenv run python app/scripts/cli.py
```

This will provide you a basic output of registered commands available. To run
a specific command:

```shell
pipenv run python app/scripts/cli.py {command_name} {-command_parameters}
```

To create your own script files, copy the `command_template.py` file in the
`app/scripts/commands` directory, rename it, create your script, then register
it in the `app/scripts/cli.py` file.

Example Registration:

```python
# Below the sys.path.append
from scripts.commands.my_new_command_from_template import my_new_command

console = Console()

@click.group()
def cli() -> None:
    pass

cli.add_command(my_new_command_from_template)

```

Though scripts can be used to create a quick test, it should be noted that they
can quickly become out of sync if they replicate logic from another service.
Consider creating scripts that interact with the designed service, report on
its resources, query its tables, trigger its resources, etc.

# Testing

This utilizes the [pytest](https://docs.pytest.org/en/7.4.x/) framework.

## Test Directory Structure

All tests are created in the `app/tests` directory. Its folder structure mirrors
the `app/src` directory and modules.

## Creating Tests

To add a new test simple create a `.py` file that begins with the work `test`;
for example: `test_bob.py`.

Each test must be prefix with `test_`:

```python
def test_bob():
    assert True
```

Tests can be nested within classes, but the class name must also being with
`Test`:

```python
class TestBobMethods:
    def test_should_call_idp(self):
        assert True
```

## Running Tests

### Simple Run

Tests can be run via the following command:

```shell
pipenv run python -m pytest app/tests
```

### Parallel Run

Test can be run in parallel with the following command:

```shell
pipenv run python -m pytest app/test -n 3
```

Where `-n` is the number of threads. It is important to note when running tests
or designing Tests to run in parallel, Parameterized Tests should have their
keys sorted (and probably not be randomized).

### Code Coverage

This project includes [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/index.html)
which can provides automatic Code Coverage reports from running `pytest`.

To create a coverage report from a pytest session run the following command:

```shell
pipenv run python -m pytest --cov=app/  app/tests
```

To narrow the scope to ignore coverage information on tests and stub builders,
run:

```shell
pipenv run python -m pytest --cov=app/src  app/tests
```

### Tip

When testing a function in a module that may have code at the module level:

```python

table_name = os.environ["SOME_VAR"]

def method_i_want_to_test():
    pass
```

The model may have to be imported within the test to properly reflect any
Mocks or fixtures setup in `pytest`:

```python

def test_method():
    from some.path import method_i_want_to_test

    response = method_i_want_to_test()

    assert response == true
```

There are alternatives to this such as reloading a module with the importlib:

```python
import some.path
from importlib import reload

reload(some.path)

def test_method():
    response = some.path.method_i_want_to_test()

    assert response == true
```

# Deploying

## Ephemeral

The CDK Infrastructure for this template is setup to accept a few command line
arguments, that will allow for multiple employees to deploy to the Ephemeral
account without collisions.

A normal deploy command would be:

```shell
cdk deploy --profile {profile-name}
```

Always specify a value for `profile`, otherwise your stack may deploy to the
undesired AWS account.

The template extend the deploy command to accept two context parameters:

- prefix
- stage

Prefix adds a name variation to the deployed stack, and lines up with what other
service may deploy. This allows services deployed with the same prefix to
communicate with each other isolation (with little effort).

```shell
cdk deploy --context prefix={name} --profile {profile-name}
```

Outside of Ephemeral (or in), a stack may be deployed with a variation of what
`stage` it is in. `stage` describes Proof Of Concept (POC),
Integration (INT), Staging (STG), and Production (PROD).

With CDK's [Aspects](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Aspects.html)
can be applied to a `stage` within the template, forcing resource to adhere to
a standard, or provide some default functionality for a set of resource.

This parameter also allows for a Production stack (with stricter permission) to
coexist in the same AWS account as a non Production stack.

To pass a stage:

```shell
cdk deploy --context stage={name} --profile {profile-name}
```

If a stage is not passed a default one is used.

For ephemeral deploys the following is recommended:

```shell
cdk deploy --context prefix={name} --context stage={stage} --profile eph-dev
```

## Deploying to Higher Environments

This is handled by GitHub Actions. Checking a branch into main will initiate
a deploy chain.
