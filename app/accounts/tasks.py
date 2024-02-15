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
            "message": "User Account Successfully Created",
            "data": data,
        }

    def create_user_error(self, data: dict):
        return {
            "status": "CREATED",
            "message": "Error Creating User Account",
            "data": data,
        }

    def password_mismatch_error(self):
        return {
            "status": "FAILED",
            "message": "Passwords do not match",
        }

    def user_does_not_exist_error(self):
        return {
            "status": "FAILED",
            "message": "User does not exist",
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

    def password_and_oldpasswordmismatch(self):
        return {
            "status": "FAILED",
            "message": "Old and New passwords must be different",
        }

    def incorrect_password_error(self):
        return {"status": "FAILED", "message": "Invalid Current Password"}


u_responses = UserResponses()
