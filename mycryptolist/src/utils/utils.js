import qs from 'qs';

class Form {

    constructor(data) {
        this.reset(data)
    }

    userData() {
        let userData = {};
        for (let field in this.fieldsData) {
            userData[field] = this[field]
        }
        return qs.stringify(userData);
    }

    isFormDisabled() {
        for (let field in this.fieldsData) {
            if (this[field].length === 0)
                return true;
        }
        return false;
    }

    reset(data) {
        this.fieldsData = data;
        for (let field in data) {
            this[field] = data[field];
        }
        this.displayForm = true;
        this.error = "";
        this.isLoading = false;
    }

    headers() {
        return {
            headers: {
                    'X-CSRFToken': window.$cookies.get('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded'
            }
        }
    }

    switchDisplay () {
        this.displayForm = !this.displayForm;
    }
}

export default Form