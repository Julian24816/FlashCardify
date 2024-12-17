<template>
  <div>
    <h1>Upload Notes</h1>
    <input type="file" @change="handleFileUpload" />
    <button @click="submitFile">Upload</button>

    <div v-if="responseText">
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
      errorMessage: ''
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
