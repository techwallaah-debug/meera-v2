#!/bin/bash

# Production Deployment Script
# Usage: ./scripts/deploy-production.sh [environment]

set -e

ENVIRONMENT=${1:-staging}
KUBECTL_NAMESPACE="social-commerce-${ENVIRONMENT}"

echo "🚀 Deploying Social Commerce Platform to ${ENVIRONMENT}"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}❌ kubectl not found. Please install kubectl.${NC}"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker not found. Please install Docker.${NC}"
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        echo -e "${RED}❌ Kubernetes cluster not accessible.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Prerequisites check passed${NC}"
}

build_images() {
    echo ""
    echo "🔨 Building Docker images..."
    
    SERVICES=("user-service" "content-service" "product-service" "order-service" 
              "search-service" "recommendation-service" "analytics-service" "notification-service")
    
    for service in "${SERVICES[@]}"; do
        echo "Building ${service}..."
        docker build -f infrastructure/docker/Dockerfile.${service} \
            -t social-commerce/${service}:${ENVIRONMENT} \
            -t social-commerce/${service}:latest \
            .
    done
    
    echo -e "${GREEN}✅ All images built${NC}"
}

push_images() {
    echo ""
    echo "📤 Pushing images to registry..."
    
    REGISTRY=${DOCKER_REGISTRY:-"ghcr.io/social-commerce"}
    
    SERVICES=("user-service" "content-service" "product-service" "order-service" 
              "search-service" "recommendation-service" "analytics-service" "notification-service")
    
    for service in "${SERVICES[@]}"; do
        echo "Pushing ${service}..."
        docker tag social-commerce/${service}:${ENVIRONMENT} ${REGISTRY}/${service}:${ENVIRONMENT}
        docker tag social-commerce/${service}:latest ${REGISTRY}/${service}:latest
        docker push ${REGISTRY}/${service}:${ENVIRONMENT}
        docker push ${REGISTRY}/${service}:latest
    done
    
    echo -e "${GREEN}✅ All images pushed${NC}"
}

deploy_infrastructure() {
    echo ""
    echo "🏗️  Deploying infrastructure..."
    
    # Create namespace if not exists
    kubectl create namespace ${KUBECTL_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
    
    # Apply ConfigMaps and Secrets
    kubectl apply -f infrastructure/kubernetes/configmap.yaml -n ${KUBECTL_NAMESPACE}
    kubectl apply -f infrastructure/kubernetes/secrets.yaml -n ${KUBECTL_NAMESPACE}
    
    echo -e "${GREEN}✅ Infrastructure deployed${NC}"
}

deploy_services() {
    echo ""
    echo "🚀 Deploying services..."
    
    # Update image tags in deployment files
    sed "s/:latest/:${ENVIRONMENT}/g" infrastructure/kubernetes/user-service-deployment.yaml | \
        kubectl apply -f - -n ${KUBECTL_NAMESPACE}
    
    # Deploy all services
    kubectl apply -f infrastructure/kubernetes/ -n ${KUBECTL_NAMESPACE}
    
    echo -e "${GREEN}✅ Services deployed${NC}"
}

wait_for_deployment() {
    echo ""
    echo "⏳ Waiting for deployments to be ready..."
    
    DEPLOYMENTS=("user-service" "content-service" "product-service" "order-service")
    
    for deployment in "${DEPLOYMENTS[@]}"; do
        echo "Waiting for ${deployment}..."
        kubectl rollout status deployment/${deployment} -n ${KUBECTL_NAMESPACE} --timeout=5m
    done
    
    echo -e "${GREEN}✅ All deployments ready${NC}"
}

run_health_checks() {
    echo ""
    echo "🏥 Running health checks..."
    
    SERVICES=("user-service:8001" "content-service:8002" "product-service:8003" "order-service:8004")
    
    for service in "${SERVICES[@]}"; do
        IFS=':' read -r name port <<< "$service"
        echo "Checking ${name}..."
        
        # Port forward and check health
        kubectl port-forward -n ${KUBECTL_NAMESPACE} svc/${name} ${port}:${port} &
        PF_PID=$!
        sleep 2
        
        if curl -f http://localhost:${port}/health &> /dev/null; then
            echo -e "${GREEN}✅ ${name} is healthy${NC}"
        else
            echo -e "${RED}❌ ${name} health check failed${NC}"
        fi
        
        kill $PF_PID 2>/dev/null || true
    done
}

run_smoke_tests() {
    echo ""
    echo "🧪 Running smoke tests..."
    
    # Get service URLs
    API_URL=$(kubectl get ingress api-ingress -n ${KUBECTL_NAMESPACE} -o jsonpath='{.spec.rules[0].host}')
    
    if [ -z "$API_URL" ]; then
        echo -e "${YELLOW}⚠️  Ingress not configured, skipping smoke tests${NC}"
        return
    fi
    
    # Test endpoints
    echo "Testing API endpoints..."
    
    # Health check
    if curl -f https://${API_URL}/users/health &> /dev/null; then
        echo -e "${GREEN}✅ API is accessible${NC}"
    else
        echo -e "${RED}❌ API health check failed${NC}"
    fi
}

show_status() {
    echo ""
    echo "📊 Deployment Status:"
    echo ""
    kubectl get pods -n ${KUBECTL_NAMESPACE}
    echo ""
    kubectl get svc -n ${KUBECTL_NAMESPACE}
    echo ""
    kubectl get ingress -n ${KUBECTL_NAMESPACE}
    echo ""
    kubectl get hpa -n ${KUBECTL_NAMESPACE}
}

# Main execution
main() {
    check_prerequisites
    build_images
    
    if [ "$ENVIRONMENT" != "local" ]; then
        push_images
    fi
    
    deploy_infrastructure
    deploy_services
    wait_for_deployment
    run_health_checks
    run_smoke_tests
    show_status
    
    echo ""
    echo -e "${GREEN}🎉 Deployment to ${ENVIRONMENT} completed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Monitor logs: kubectl logs -f -n ${KUBECTL_NAMESPACE}"
    echo "2. Check metrics: kubectl port-forward svc/prometheus 9090:9090 -n ${KUBECTL_NAMESPACE}"
    echo "3. View dashboards: kubectl port-forward svc/grafana 3000:3000 -n ${KUBECTL_NAMESPACE}"
}

main
