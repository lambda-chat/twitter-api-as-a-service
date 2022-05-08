#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { TwitterApiAsAServiceStack } from '../lib/twitter-api-as-a-service-stack';

const app = new cdk.App();
new TwitterApiAsAServiceStack(app, 'TwitterApiAsAServiceStack');
