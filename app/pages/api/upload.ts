import formidable from 'formidable';
import fs from 'fs';
import { spawn } from 'child_process';

// Disable body parsing for file uploads
export const config = {
  api: {
    bodyParser: false,
  },
};

export default function handler(req, res) {
  if (req.method === 'POST') {
    const form = formidable({ uploadDir: './public/files', keepExtensions: true });

    form.parse(req, (err, fields, files) => {
      if (err) {
        return res.status(500).json({ error: 'File upload failed' });
      }

      const uploadedFile = files.file[0].filepath; // Path to uploaded file

      // Run OCR using Tesseract
      const tesseract = spawn('tesseract', [uploadedFile, 'stdout', '-l', 'deu']);

      let ocrText = '';
      tesseract.stdout.on('data', (data) => {
        ocrText += data.toString();
      });

      tesseract.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
      });

      tesseract.on('close', (code) => {
        if (code !== 0) {
          return res.status(500).json({ error: 'Tesseract OCR failed' });
        }
        res.status(200).json({ text: ocrText });
      });
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
