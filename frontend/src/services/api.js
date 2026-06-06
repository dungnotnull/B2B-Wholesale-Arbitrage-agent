import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const sourcingService = {
  async searchProducts(imageData) {
    const response = await api.post('/api/v1/source', { image: imageData });
    return response.data;
  },
  async getSuppliers(productId) {
    const response = await api.get(`/api/v1/suppliers?product_id=${productId}`);
    return response.data;
  },
  async startNegotiation(supplierId, script) {
    const response = await api.post(`/api/v1/negotiate`, { supplier_id: supplierId, script });
    return response.data;
  }
};
