
# Pocket Masters

This is a project with two functions for me

1. To test and learn how to build and configure aws resources
2. To build some interesting functionality

This is a project built using AWS CDK using python. For more information on AWS CDK see [here](https://docs.aws.amazon.com/cdk/v2/guide/home.html) 

## Dependancies

Below is a list of dependencies that are required to be on your local machine to be able to work with the project

- python3 `python3 --version`
- cdk `cdk --version`

This list are dependencies are 

- [sam cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) `sam --version`

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



### Unit tests
There is also a very trivial test included that can be run like this:

```
$ pytest
```

### Testing Serverless Locally

SAM cli can be used to test serverless applications that have been built using cdk, for further infromation see [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-cdk-testing.html)


To start run
```
cdk synth
```

Then usage for sam is as below 
```
# Invoke the function FUNCTION_IDENTIFIER declared in the stack STACK_NAME
sam local invoke -t ./cdk.out/pocket-masters-api.template.json ApiMethodFunction

# Start all APIs declared in the AWS CDK application
sam local start-api -t ./cdk.out/pocket-masters-api.template.json [OPTIONS]

# Start a local endpoint that emulates AWS Lambda
sam local start-lambda -t ./cdk.out/CdkSamExampleStack.template.json [OPTIONS]
```

```
sam build -t ./cdk.out/pocket-masters-api.template.json
```

## Deploying Changes
You can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```
