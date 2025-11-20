// *******************************
// AgendaFácil – Full‑Stack Scheduler
// Tech Stack: Node.js + Express + MongoDB (Mongoose) + React (Vite) + TailwindCSS
// Extras: Twilio (WhatsApp) & Stripe for payments
// *******************************
//
// ╔══════════════╗
// ║ File Tree ║
// ╚══════════════╝
// agenda-facil/
// ├── backend/
// │   ├── package.json
// │   ├── server.js
// │   ├── .env.example
// │   ├── config/
// │   │   └── db.js
// │   ├── models/
// │   │   ├── User.js
// │   │   ├── Service.js
// │   │   └── Booking.js
// │   ├── routes/
// │   │   ├── auth.js
// │   │   ├── services.js
// │   │   └── bookings.js
// │   └── utils/
// │       └── whatsapp.js
// └── frontend/
//     ├── package.json
//     ├── vite.config.js
//     ├── index.html
//     ├── src/
//     │   ├── main.jsx
//     │   ├── App.jsx
//     │   ├── api.js
//     │   ├── components/
//     │   │   ├── Navbar.jsx
//     │   │   ├── Hero.jsx
//     │   │   ├── Pricing.jsx
//     │   │   └── BookingForm.jsx
//     │   └── pages/
//     │       ├── Home.jsx
//     │       ├── Dashboard.jsx
//     │       └── BookingPage.jsx
//     └── tailwind.config.cjs
//
// ───────────────────────────────────
// BACKEND
// ───────────────────────────────────
/* backend/package.json */
{
  "name": "agenda-facil-api",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.0.3",
    "express": "^4.18.2",
    "mongoose": "^8.0.3",
    "stripe": "^14.0.0",
    "twilio": "^4.18.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}

/* backend/.env.example */
PORT=5000
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.mongodb.net/agendafacil
STRIPE_SECRET=sk_test_xxxxxxxxx
TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

/* backend/config/db.js */
import mongoose from 'mongoose';
export const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log('MongoDB connected');
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
};

/* backend/models/Service.js */
import mongoose from 'mongoose';
const ServiceSchema = new mongoose.Schema({
  owner: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  name: { type: String, required: true },
  duration: { type: Number, required: true }, // minutes
  price: { type: Number, required: true }
}, { timestamps: true });
export default mongoose.model('Service', ServiceSchema);

/* backend/models/Booking.js */
import mongoose from 'mongoose';
const BookingSchema = new mongoose.Schema({
  service: { type: mongoose.Schema.Types.ObjectId, ref: 'Service', required: true },
  clientName: String,
  clientPhone: String,
  start: Date,
  end: Date,
  paid: { type: Boolean, default: false }
}, { timestamps: true });
export default mongoose.model('Booking', BookingSchema);

/* backend/routes/services.js */
import express from 'express';
import Service from '../models/Service.js';
const router = express.Router();
// GET all services for owner
router.get('/', async (req, res) => {
  const owner = req.query.owner;
  const services = await Service.find({ owner });
  res.json(services);
});
// POST create new service
router.post('/', async (req, res) => {
  const service = await Service.create(req.body);
  res.json(service);
});
export default router;

/* backend/utils/whatsapp.js */
import twilio from 'twilio';
const client = twilio(process.env.TWILIO_SID, process.env.TWILIO_TOKEN);
export const sendWhatsApp = async (to, message) => {
  return client.messages.create({
    from: `whatsapp:${process.env.TWILIO_WHATSAPP_FROM}`,
    to: `whatsapp:${to}`,
    body: message
  });
};

/* backend/routes/bookings.js */
import express from 'express';
import Booking from '../models/Booking.js';
import Service from '../models/Service.js';
import { sendWhatsApp } from '../utils/whatsapp.js';
const router = express.Router();
// POST create booking
router.post('/', async (req, res) => {
  const { serviceId, clientName, clientPhone, start } = req.body;
  const service = await Service.findById(serviceId);
  const end = new Date(new Date(start).getTime() + service.duration * 60000);
  const booking = await Booking.create({ service: serviceId, clientName, clientPhone, start, end });
  // Send WhatsApp confirmation
  await sendWhatsApp(clientPhone, `Olá ${clientName}, sua reserva para ${service.name} está confirmada em ${new Date(start).toLocaleString('pt-BR')}. Até breve!`);
  res.json(booking);
});
export default router;

/* backend/server.js */
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { connectDB } from './config/db.js';
import serviceRoutes from './routes/services.js';
import bookingRoutes from './routes/bookings.js';

dotenv.config();
connectDB();
const app = express();
app.use(cors());
app.use(express.json());
app.use('/api/services', serviceRoutes);
app.use('/api/bookings', bookingRoutes);
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

// ───────────────────────────────────
// FRONTEND (Vite + React + Tailwind)
// ───────────────────────────────────
/* frontend/package.json */
{
  "name": "agenda-facil-client",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.7.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.23.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.24",
    "tailwindcss": "^3.4.1",
    "vite": "^5.1.0"
  }
}

/* frontend/vite.config.js */
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  server: { port: 5173 }
});

/* frontend/src/api.js */
import axios from 'axios';
export const api = axios.create({ baseURL: 'http://localhost:5000/api' });

/* frontend/src/main.jsx */
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import './index.css';
ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);

/* frontend/src/App.jsx */
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import BookingPage from './pages/BookingPage.jsx';
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/:owner/book" element={<BookingPage />} />
    </Routes>
  );
}

/* frontend/src/pages/Home.jsx */
import Navbar from '../components/Navbar.jsx';
import Hero from '../components/Hero.jsx';
import Pricing from '../components/Pricing.jsx';
export default function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <Pricing />
    </>
  );
}

/* frontend/src/pages/BookingPage.jsx */
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { api } from '../api.js';
import BookingForm from '../components/BookingForm.jsx';
export default function BookingPage() {
  const { owner } = useParams();
  const [services, setServices] = useState([]);
  useEffect(() => {
    api.get(`/services?owner=${owner}`).then(r => setServices(r.data));
  }, [owner]);
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <BookingForm services={services} />
    </div>
  );
}

/* frontend/src/components/BookingForm.jsx */
import { useState } from 'react';
import { api } from '../api.js';
export default function BookingForm({ services }) {
  const [data, setData] = useState({ serviceId: '', clientName: '', clientPhone: '', start: '' });
  const handleSubmit = e => {
    e.preventDefault();
    api.post('/bookings', data).then(() => alert('Reserva realizada!')).catch(console.error);
  };
  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md bg-white p-6 rounded-2xl shadow-xl space-y-4">
      <h2 className="text-xl font-bold text-center">Agendar Horário</h2>
      <select className="w-full border p-2" value={data.serviceId} onChange={e => setData({ ...data, serviceId: e.target.value })} required>
        <option value="">Escolha um serviço</option>
        {services.map(s => <option key={s._id} value={s._id}>{s.name} – {s.duration}min – R$ {s.price}</option>)}
      </select>
      <input className="w-full border p-2" placeholder="Nome" value={data.clientName} onChange={e => setData({ ...data, clientName: e.target.value })} required />
      <input className="w-full border p-2" placeholder="WhatsApp (DDD+Número)" value={data.clientPhone} onChange={e => setData({ ...data, clientPhone: e.target.value })} required />
      <input type="datetime-local" className="w-full border p-2" value={data.start} onChange={e => setData({ ...data, start: e.target.value })} required />
      <button className="w-full bg-indigo-600 text-white py-2 rounded-xl hover:bg-indigo-700" type="submit">Confirmar</button>
    </form>
  );
}

/* frontend/tailwind.config.cjs */
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: { extend: {} },
  plugins: []
};

/* frontend/src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

// *******************************
// Quick Start
// 1. Clone repo & run: cd backend && npm i && npm run dev
// 2. In new terminal: cd frontend && npm i && npm run dev
// 3. Access: http://localhost:5173
// 4. Create a service via POST /api/services or seed DB, then share /<owner>/book link.
// *******************************
