import google.auth
import datetime
from google.cloud.container_v1 import ClusterManagerClient
from google.oauth2 import service_account
from google.auth import compute_engine
from kubernetes import client, config
from google.cloud import container_v1
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp

def check_gke_cluster_health(project_id, location, cluster_name, credentials_path):
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )    
    clientmanager = ClusterManagerClient(credentials=credentials)

    response = clientmanager.get_cluster(
        name=f'projects/{project_id}/locations/{location}/clusters/{cluster_name}'
    )

    # Check cluster status
    if response.status == container_v1.Cluster.Status.RUNNING:
        print("Cluster is running.")
    else:
        print(f"Cluster is in {response.status} state. Check cluster health.")

    client_monitor = monitoring_v3.MetricServiceClient(credentials=credentials)
    project_name = f"projects/{project_id}"
    cluster_resource_type = "k8s_container"
    cluster_metric_type = "kubernetes.io/container/cpu/core_usage_time"
# Set time range for the query
    metric_types = client_monitor.list_metric_descriptors(name=project_name)

    # for metric_type in metric_types:
    #     print(f"Available Metric Type: {metric_type.type}")

    start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
    end_time = datetime.datetime.utcnow()

    interval = monitoring_v3.TimeInterval(
        start_time=start_time, end_time=end_time
    )
    query = f'resource.type="{cluster_resource_type}" AND resource.label.cluster_name="{cluster_name}" AND metric.type="{cluster_metric_type}"'

    results = client_monitor.list_time_series(
      request={
        "name": project_name,
        "filter": query,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    print(results)

    # for time_series in results:
    #     for point in time_series.points:
    #         print(
    #             f"CPU usage for GKE Cluster {cluster_name}: {point.value.double_value}"
    #         )



if __name__ == "__main__":
    # Replace these values with your GKE cluster information
    project_id = "parabolic-hook-412914"
    location = "us-central1"
    cluster_name = "autopilot-cluster-1"
    credentials_path = "credentials.json"

    check_gke_cluster_health(project_id, location, cluster_name, credentials_path)
