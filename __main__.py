import pulumi
import pulumi_azure_native as azure_native
from datetime import datetime, timedelta

# Retrieve the Azure subscription ID
client_config = azure_native.authorization.get_client_config()
subscription_id = client_config.subscription_id

# Define the scope for the budget
scope = f"/subscriptions/{subscription_id}"
email = "wi22b116@technikum-wien.at"

# Specify the time period for the budget
start_date = datetime(2024, 11, 1).strftime("%Y-%m-%d")
end_date = datetime(2025, 11, 1).strftime("%Y-%m-%d")

# Create the budget resource
budget = azure_native.consumption.Budget("myBudget",
    budget_name="myBudget",
    scope=scope,
    amount=80.0,
    time_grain="Monthly",
    time_period={
        "start_date": start_date,
        "end_date": end_date,
    },
    notifications={
        "Actual_GreaterThan_80_Percent": azure_native.consumption.NotificationArgs(
            enabled=True,
            operator="GreaterThan",
            threshold=80,
            contact_emails=[email],
            contact_roles=["Contributor"],
            threshold_type="Actual",
            locale="en-us",
        ),
        "Forecasted_GreaterThan_90_Percent": azure_native.consumption.NotificationArgs(
            enabled=True,
            operator="GreaterThan",
            threshold=90,
            contact_emails=[email],
            contact_roles=["Contributor"],
            threshold_type="Forecasted",
            locale="en-us",
        ),
    },
    category="Cost",
)


pulumi.export("budget_id", budget.id)
