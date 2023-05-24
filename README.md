
# Project Orion

This is a project with two functions for me

1. To test and learn how to build and configure aws resources
2. To build some interesting functionality

This is a project built using AWS CDK using python. For more information on AWS CDK see [here](https://docs.aws.amazon.com/cdk/v2/guide/home.html) 

## Dependancies

### Local

Below is a list of dependencies that are required to be on your local machine to be able to work with the project

- python3 `python3 --version`
- cdk `cdk --version`

This list are dependencies are 

- [sam cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) `sam --version`

### AWS Account

There are some one of manual steps that are required to be run once when deploying to a new account.

- ensure each environment you are deploying into has been bootstraped with `cdk bootstrap`
- update the pending codestar [connection](https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html) with the active repo 


## Getting Started
To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

You can then install the dev dependencies.
```
$ pip install -r requirements-dev.txt
```


To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.



## Development

The `cdk.json` file tells the CDK Toolkit how to execute your app.

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Testing Locally
Before every logic change commit, code should be synthed and deployed successfully 

For more information on how to deploy locally see the [Deploying Changes](#deploying-changes) section below

### Unit tests
There is also unit tests included that can be with `pytest`:

### Testing Serverless Locally

SAM cli can be used to test serverless applications that have been built using cdk, for further infromation see [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-cdk-testing.html)


To start ensure your code has been synthed with `cdk synth "<Stage>/*`

CDK stores stages in `cdk.out/assembly-<StageName>/<StackName><Descriminator>.template.json`

Some local testing commands require environment variables passed through the CLI.
These env vars are to be stored in the `config/local/` folder though this is not committed to version control 
as tracking changes might impact local testing of others. To see the structure of the file see 
[SAMs Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-invoke.html#serverless-sam-cli-using-invoke-environment-file). This file can
be passed using the `--env-vars` argument

#### Lambdas

To test a lambda function you can invoke with the command below
```
# Invoke the function FUNCTION_IDENTIFIER declared in the stack STACK_NAME
sam local invoke -t ./cdk.out/orion-api.template.json ApiMethodFunction
```

#### APIs

```
# Start all APIs declared in the AWS CDK application
sam local start-api -t ./cdk.out/assembly-OrionApp/OrionAppApiA21C1F57.template.json [OPTIONS]
```

```
sam build -t ./cdk.out/orion-api.template.json
```

## Deploying Changes
### Locally
You can now synthesize the CloudFormation template for this code. This will check that your code compiles

```
cdk synth '<StageId>/*'
```

To deploy a from your local repo you can deploy any stage with
```
cdk deploy '<StageId>/*'
```

### Remotely
There is a CodePipeline that is created witht this deployment that will deploy all changes when pushed to main




