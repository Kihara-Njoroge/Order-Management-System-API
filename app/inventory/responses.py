class Responses:
    def create_product_success(self, data: dict):
        return {
            "status": "CREATED",
            "message": "Product successfully created",
            "data": data,
        }

    def create_product_error(self, data: dict):
        return {
            "status": "FAILED",
            "message": "Error creating product",
            "data": data
        }

    def update_product_success(self, data):
        return {
            "status": "SUCCESS",
            "message": "Product updated successfully",
            "data": data,
        }

    def update_product_error(self):
        return {"status": "FAILED", "message": "Product update failed"}

    def delete_product_success(self, data):
        return {
            "status": "SUCCESS",
            "message": "Product deleted successfully",
            "data": data,
        }

    def get_products_success(self, data):
        if isinstance(data, list):
            return {
                "status": "SUCCESS",
                "message": "Products retrieved successfully",
                "data": data
            }
        else:
            return {
                "status": "SUCCESS",
                "message": "Product retrieved successfully",
                "data": data
            }

    def create_category_success(self, data: dict):
        return {
            "status": "CREATED",
            "message": "Category successfully created",
            "data": data,
        }

    def create_category_error(self, data: dict):
        return {
            "status": "FAILED",
            "message": "Error creating category",
            "data": data
        }

    def update_category_success(self, data):
        return {
            "status": "SUCCESS",
            "message": "Category updated successfully",
            "data": data,
        }

    def update_category_error(self):
        return {"status": "FAILED", "message": "Category update failed"}

    def delete_category_success(self, data):
        return {
            "status": "SUCCESS",
            "message": "Category deleted successfully",
            "data": data,
        }

    def get_categories_success(self, data):
        if isinstance(data, list):
            return {
                "status": "SUCCESS",
                "message": "Categories retrieved successfully",
                "data": data
            }
        else:
            return {
                "status": "SUCCESS",
                "message": "Category retrieved successfully",
                "data": data
            }