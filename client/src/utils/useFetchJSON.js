

export const useFetchJSON = () => {
    const handleRequest = async (url, method, body = null, csrfToken = null) => {
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrfToken,
        }
        const configObj = {
            method,
            headers,
            body: body ? JSON.stringify(body) : null,
        }
        try {
            const res = await fetch(url, configObj)
            if (!res.ok) {
                const errorBody = await res.json();
                throw new Error(errorBody.message || 'Request Failed: status: ' + res.status)
            }
            debugger
            return res.json()
        } 
        catch (error) {
            console.error(`Error in ${method} request to ${url}: ${error.message}`); //
            throw new Error(error.message || 'Failed to Fetch: Is the server running?')
        }
    }

    const postJSON = async (url, formData, csrfToken) => {
        return await handleRequest(url, 'POST', formData, csrfToken )
    }

    const patchJSON = async (url, formData, csrfToken) => {
        debugger
        return await handleRequest(`${url}`, 'PATCH', formData, csrfToken)
    }

    const deleteJSON = async (url, csrfToken) => {
        debugger
        return await handleRequest(`${url}`, 'DELETE', csrfToken)
    }

    return { postJSON, patchJSON, deleteJSON }
}

export default useFetchJSON