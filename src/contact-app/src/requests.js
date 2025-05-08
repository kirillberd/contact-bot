import axios from "axios";

const API_LINK = process.env.REACT_APP_API_URL;

const apiClient = axios.create({
  baseURL: API_LINK,
  headers: {
    "api-key": process.env.REACT_APP_AUTH_TOKEN,
  },

});

async function fetchContacts(payload) {
  console.log(process.env.REACT_APP_AUTH_TOKEN)
  try {
    const response = await apiClient.get("/contacts", {
      params: {
        tags: payload?.tags,
        region: payload?.region,
      },
    });
    console.log("Contacts fetched:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching contacts:", error);
  }
}

async function insertContact(payload) {
  try {
    const response = await apiClient.post("/insert-contact", payload);
    console.log("Contact inserted:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error inserting contact:", error);
  }
}

async function updateContact(payload, id) {
  try {
    const response = await apiClient.put(`/contacts/${id}`, payload);
    return response.data;
  } catch (error) {
    console.error("Error updating contact:", error);
  }
}

async function deleteContact(id) {
  try {
    const response = await apiClient.delete(`/contacts/${id}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting contact:", error);
  }
}

export { fetchContacts, insertContact, updateContact, deleteContact };
