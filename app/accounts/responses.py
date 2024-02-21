class UserResponses:
    def user_exists_error(self, data):
        return {
            "status": "FAILED",
            "message": "User with these credentials already exists.",
            "data": data,
        }

    def user_created_success(self, data: dict):
        return {
            "status": "CREATED",
            "message": "User Account successfully Created",
            "data": data,
        }

    def create_user_error(self, data: dict):
        return {
            "status": "FAILED",
            "message": "Error Creating User Account",
            "data": data
        }

    def password_mismatch_error(self):
        return {
            "status": "FAILED",
            "message": "Password Mismatch. Passwords do not match",
        }

    def user_update_success(self, data):
        return {
            "status": "SUCCESS",
            "message": "User Account Updated Successfully",
            "data": data,
        }

    def user_update_error(self):
        return {"status": "FAILED", "message": "User update failed"}

    def password_change_success(self):
        return {"status": "SUCCESS", "message": "Password successfully changed"}

    def password_and_confirmpassword_mismatch(self):
        return {
            "status": "FAILED",
            "message": "Password and confirm password must be the same",
        }

    def password_and_oldpasswordmismatch(self):
        return {
            "status": "FAILED",
            "message": "Old and New passwords must be different",
        }

    def incorrect_password_error(self):
        return {"status": "FAILED", "message": "Invalid Current Password"}

    def delete_user_success(self, data):
        return {
            "status": "SUCCESS",
            "message": "User account successfully deleted",
            "data": data,
        }

    def get_user_success(self, data):
        if isinstance(data, list):
            return {
                "status": "SUCCESS",
                "message": "User accounts retrieved successfully.",
                "data": data
            }
        else:
            return {
                "status": "SUCCESS",
                "message": "User account retrieved successfully.",
                "data": data
            }