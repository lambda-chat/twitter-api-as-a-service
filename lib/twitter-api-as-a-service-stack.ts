import * as path from 'path';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import {config} from 'dotenv';
import { HttpMethod } from 'aws-cdk-lib/aws-lambda';

type Environment = {
  ApiKey: string;
  ApiSecretKey: string;
  AccessToken: string;
  AccessTokenSecret: string;
  LambdaApiKey: string;
}

const environment = config().parsed as Environment;

export class TwitterApiAsAServiceStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const pythonPackageLayer = new lambda.LayerVersion(this, "PythonPackages", {
      code: lambda.Code.fromAsset(path.join(__dirname, "..", "layer")),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
      description: "Python Packages",
    });

    const lambdaFunction = new lambda.Function(this, "TwitterApiAsAService", {
      functionName: "twitter-api-as-a-service",
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "app.handler",
      code: lambda.Code.fromAsset(path.join(__dirname, "..", "lambda")),
      layers: [pythonPackageLayer],
      environment,
      retryAttempts: 1,
      timeout: cdk.Duration.seconds(2),
    });

    void new lambda.FunctionUrl(this, "TwitterApiAsAServiceUrl", {
      function: lambdaFunction,
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        allowedMethods: [HttpMethod.GET],
        allowedOrigins: ["https://api.twitter.com"],
      },
    })
  }
}
