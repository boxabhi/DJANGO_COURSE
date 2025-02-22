import React, { useState, useEffect } from "react";
import { Container, Card, CardContent, Typography, LinearProgress, Button, Chip, Box, Select, MenuItem } from "@mui/material";
import axios from "axios";

const App = () => {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [responseData, setResponseData] = useState(null);
  const [jobDescriptions, setJobDescriptions] = useState([]);
  const [selectedJob, setSelectedJob] = useState("");

  useEffect(() => {
    fetchJobDescriptions();
  }, []);

  const fetchJobDescriptions = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/jobs/");
      if (response.data.status) {
        setJobDescriptions(response.data.data);
      } else {
        alert("Failed to fetch job descriptions.");
      }
    } catch (error) {
      console.error("Error fetching job descriptions:", error);
      alert("Could not fetch job descriptions.");
    }
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }
    if (!selectedJob) {
      alert("Please select a job description first!");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", selectedJob);

    try {
      const response = await axios.post("http://127.0.0.1:8000/resume/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percentCompleted);
        },
      });

      setResponseData(response.data.data);
      
      
      
    } catch (error) {
      console.error("Upload failed", error);
      alert("Upload failed. Please try again.");
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 5 }}>
      <Card sx={{ p: 3, boxShadow: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>Upload a PDF</Typography>

          {/* Job Description Dropdown */}
          <Typography variant="subtitle1" sx={{ mt: 2 }}>Select Job Description:</Typography>
          <Select
            fullWidth
            value={selectedJob}
            onChange={(e) => setSelectedJob(e.target.value)}
            sx={{ mt: 1 }}
          >
            {jobDescriptions.map((job) => (
              <MenuItem key={job.id} value={job.id}>
                {job.job_title}
              </MenuItem>
            ))}
          </Select>

          {/* File Upload */}
          <Typography variant="subtitle1" sx={{ mt: 3 }}>Upload Resume (PDF):</Typography>
          <input type="file" accept="application/pdf" onChange={handleFileChange} />

          <Button variant="contained" color="primary" onClick={handleUpload} sx={{ mt: 2 }}>
            Upload
          </Button>

          {progress > 0 && (
            <>
              <Typography sx={{ mt: 2 }}>Uploading: {progress}%</Typography>
              <LinearProgress variant="determinate" value={progress} sx={{ mt: 1 }} />
            </>
          )}

         {/* Response Data */}
{responseData && (
  <Box sx={{ mt: 3 }}>
    <Typography variant="h6">Rank: {responseData.rank}</Typography>
    <Typography variant="h6">Total Experience: {responseData.total_experience} years</Typography>

    {/* Check if skills exist before mapping */}
    {responseData.skills?.length > 0 && (
      <>
        <Typography variant="h6" sx={{ mt: 2 }}>Skills:</Typography>
        {responseData.skills.map((skill, index) => (
          <Chip key={index} label={skill} sx={{ m: 0.5 }} />
        ))}
      </>
    )}

    {/* Check if project_category exists before mapping */}
    {responseData.project_category?.length > 0 && (
      <>
        <Typography variant="h6" sx={{ mt: 2 }}>Project Categories:</Typography>
        {responseData.project_category.map((category, index) => (
          <Chip key={index} label={category} color="secondary" sx={{ m: 0.5 }} />
        ))}
      </>
    )}
  </Box>
)}

        </CardContent>
      </Card>
    </Container>
  );
};

export default App;
