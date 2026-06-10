"""Tests for orders API endpoints."""
import pytest


class TestOrdersEndpoints:
    """Test suite for orders-related endpoints."""

    def test_get_all_orders(self, client):
        """Test getting all orders returns a non-empty list with required fields."""
        response = client.get("/api/orders")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        first_order = data[0]
        assert "id" in first_order
        assert "order_number" in first_order
        assert "customer" in first_order
        assert "status" in first_order
        assert "warehouse" in first_order
        assert "order_date" in first_order
        assert "total_value" in first_order

    def test_get_orders_by_warehouse(self, client):
        """Test filtering orders by warehouse returns only matching results."""
        response = client.get("/api/orders?warehouse=Tokyo")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for order in data:
            assert order["warehouse"] == "Tokyo"

    def test_get_orders_by_category(self, client):
        """Test filtering orders by category returns only matching results (case-insensitive)."""
        response = client.get("/api/orders?category=Sensors")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for order in data:
            assert order["category"].lower() == "sensors"

    def test_get_orders_by_status(self, client):
        """Test filtering orders by status returns only matching results."""
        response = client.get("/api/orders?status=Delivered")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for order in data:
            assert order["status"] == "Delivered"

    def test_get_orders_by_month(self, client):
        """Test filtering orders by month returns only orders from that month."""
        response = client.get("/api/orders?month=2025-03")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for order in data:
            assert order["order_date"].startswith("2025-03")

    def test_get_orders_by_quarter(self, client):
        """Test filtering orders by quarter returns only orders in that quarter."""
        response = client.get("/api/orders?month=Q1-2025")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for order in data:
            month_num = int(order["order_date"][5:7])
            assert month_num in (1, 2, 3)
            assert order["order_date"].startswith("2025-")

    def test_get_orders_multiple_filters(self, client):
        """Test combining warehouse, category, and status filters."""
        response = client.get("/api/orders?warehouse=London&category=Actuators&status=Shipped")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        for order in data:
            assert order["warehouse"] == "London"
            assert order["category"].lower() == "actuators"
            assert order["status"] == "Shipped"

    def test_get_orders_filter_all_value(self, client):
        """Test that warehouse=all returns the same count as no filter."""
        response_all = client.get("/api/orders?warehouse=all")
        response_no_filter = client.get("/api/orders")

        assert response_all.status_code == 200
        assert response_no_filter.status_code == 200

        assert len(response_all.json()) == len(response_no_filter.json())

    def test_get_order_by_id(self, client):
        """Test fetching a specific order by ID returns the correct order."""
        all_response = client.get("/api/orders")
        all_orders = all_response.json()
        assert len(all_orders) > 0

        first_id = all_orders[0]["id"]

        response = client.get(f"/api/orders/{first_id}")
        assert response.status_code == 200

        order = response.json()
        assert order["id"] == first_id

    def test_get_nonexistent_order(self, client):
        """Test that fetching a non-existent order returns 404 with 'not found' in detail."""
        response = client.get("/api/orders/nonexistent-order-999")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_order_items_structure(self, client):
        """Test that order items contain required fields with correct types."""
        response = client.get("/api/orders")
        data = response.json()
        assert len(data) > 0

        first_order = data[0]
        assert "items" in first_order
        assert isinstance(first_order["items"], list)
        assert len(first_order["items"]) > 0

        first_item = first_order["items"][0]
        assert "sku" in first_item
        assert "name" in first_item
        assert "quantity" in first_item
        assert "unit_price" in first_item
        assert isinstance(first_item["quantity"], int)
        assert isinstance(first_item["unit_price"], (int, float))

    def test_order_status_values(self, client):
        """Test that all order statuses are within the expected set."""
        response = client.get("/api/orders")
        data = response.json()
        assert len(data) > 0

        valid_statuses = {"delivered", "shipped", "processing", "backordered"}
        for order in data:
            assert order["status"].lower() in valid_statuses

    def test_order_dates_format(self, client):
        """Test that order dates follow expected format conventions."""
        response = client.get("/api/orders")
        data = response.json()
        assert len(data) > 0

        for order in data:
            assert "2025-" in order["order_date"]
            assert "T" in order["expected_delivery"]

    def test_order_total_value_calculation(self, client):
        """Test that total_value equals sum of quantity times unit_price within tolerance."""
        response = client.get("/api/orders")
        data = response.json()
        assert len(data) > 0

        for order in data[:10]:
            calculated = sum(
                item["quantity"] * item["unit_price"]
                for item in order["items"]
            )
            assert abs(order["total_value"] - calculated) < 0.01

    def test_order_warehouse_values(self, client):
        """Test that all order warehouses are within the expected set."""
        response = client.get("/api/orders")
        data = response.json()
        assert len(data) > 0

        valid_warehouses = {"San Francisco", "London", "Tokyo"}
        for order in data:
            assert order["warehouse"] in valid_warehouses
