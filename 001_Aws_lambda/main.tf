terraform {
        required_providers {
            archive = {
                source = "hashicorp/archive"
            }

            aws = {
                source = "hashicorp/aws"

            }

        }

}

provider "aws" {
    access_key=""
    secret_key=""
    region="us-east-1"

}

locals {
    function_name="battery_health_check_tf"
    handler="lambda_function.lambda_handler"
    runtime="python3.12"
    timeout=6
    zip_file=".\\zip\\battery_health_check_terraform.zip"
}

data "aws_iam_policy_document" "default_tf" {
	version = "2012-10-17"

	statement {
		
		actions = ["sts:AssumeRole"]
		effect = "Allow"

		principals {
			identifiers = ["lambda.amazonaws.com"]
			type = "Service"
		}
	}
}
resource "aws_iam_role" "default_tf" {
	
	assume_role_policy = data.aws_iam_policy_document.default_tf.json
	
}
resource "aws_iam_role_policy_attachment" "default_tf" {
	policy_arn  = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
	role = aws_iam_role.default_tf.name
}

resource "aws_lambda_function" "default_tf" {
	// Function parameters we defined at the beginning
	function_name = local.function_name
	handler = local.handler
	runtime = local.runtime
	timeout = local.timeout

	// Upload the .zip file Terraform created to AWS
	filename = local.zip_file
	
	// Connect our IAM resource to our lambda function in AWS
	role = aws_iam_role.default_tf.arn
}

resource "aws_lambda_invocation" "example" {
  function_name = aws_lambda_function.default_tf.function_name

  input = jsonencode({
"device": "Battery1",
"payload": "F1E6E63676C75000"
})
}

output "result_entry" {
  value = jsondecode(aws_lambda_invocation.example.result)
}