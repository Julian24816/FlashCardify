<template>
  <div>
    <h1>Upload Notes</h1>
    <input type="file" @change="handleFileUpload" />
    <button @click="submitFile">Upload</button>

    <div v-if="responseText">
      <button @click="downloadCSV">Download CSV</button>
      <h2>Extracted Text:</h2>
      <pre>{{ responseText }}</pre>
    </div>
    <div v-if="errorMessage">
      <h2>Error:</h2>
      <p>{{ errorMessage }}</p>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      responseText: '',
      errorMessage: '',
      apiUrl: "http://127.0.0.1:5000/api/download_csv", // Replace with your API endpoint
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async submitFile() {
      if (!this.selectedFile) {
        alert('Please select a file first!');
        return;
      }

      let formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.responseText = response.data.text;
        this.errorMessage = '';
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Something went wrong!';
        this.responseText = '';
      }
    },
    async downloadCSV() {
      try {
        // 1. Fetch the file directly as a blob
        const response = await fetch(this.apiUrl, {
          method: "GET",
          headers: {
            Accept: "text/csv", // Request CSV format
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch the CSV file from the API.");
        }

        // 2. Get the response as a Blob
        const blob = await response.blob();

        // 3. Trigger a download
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "data.csv"; // Set the desired filename
        link.click();

        // 4. Cleanup
        URL.revokeObjectURL(link.href);
      } catch (error) {
        console.error("Error downloading the file:", error);
        alert("Failed to download the file.");
      }
    }
  }
};
</script>

<style scoped>
div {
  margin: 20px;
}

input {
  margin-bottom: 10px;
}
</style>
