#!/bin/bash

# Cloud Deployment Script
# Usage: ./scripts/deploy-cloud.sh [aws|gcp|azure] [environment]

set -e

CLOUD_PROVIDER=${1:-aws}
ENVIRONMENT=${2:-production}

echo "☁️  Deploying to ${CLOUD_PROVIDER} (${ENVIRONMENT})"
echo ""

case $CLOUD_PROVIDER in
  aws)
    echo "🚀 Deploying to AWS..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
      echo "❌ AWS CLI not found. Please install AWS CLI."
      exit 1
    fi
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
      echo "❌ Terraform not found. Please install Terraform."
      exit 1
    fi
    
    cd infrastructure/terraform
    
    # Initialize Terraform
    echo "📦 Initializing Terraform..."
    terraform init
    
    # Plan deployment
    echo "📋 Planning deployment..."
    terraform plan -var="environment=${ENVIRONMENT}" -out=tfplan
    
    # Apply deployment
    echo "🚀 Applying deployment..."
    terraform apply tfplan
    
    # Get outputs
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    terraform output
    
    # Configure kubectl
    echo ""
    echo "🔧 Configuring kubectl..."
    eval $(terraform output -raw kubectl_config_command)
    
    # Deploy Kubernetes resources
    echo ""
    echo "☸️  Deploying Kubernetes resources..."
    cd ../kubernetes
    kubectl apply -f .
    
    echo ""
    echo "🎉 AWS deployment complete!"
    ;;
    
  gcp)
    echo "🚀 Deploying to GCP..."
    echo "⚠️  GCP deployment configuration coming soon"
    ;;
    
  azure)
    echo "🚀 Deploying to Azure..."
    echo "⚠️  Azure deployment configuration coming soon"
    ;;
    
  *)
    echo "❌ Invalid cloud provider. Use: aws, gcp, or azure"
    exit 1
    ;;
esac
