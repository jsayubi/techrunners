import { createStore } from 'vuex';
import axios from 'axios';

// API endpoint
const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000';

export default createStore({
	state: {
		messages: [],
		conversationId: null,
		clientId: null,
		isLoading: false,
		error: null,
		requirements: [],
		pricing: null,
		orderStatus: null,
	},
	getters: {
		getMessages: (state) => state.messages,
		isLoading: (state) => state.isLoading,
		getError: (state) => state.error,
		getRequirements: (state) => state.requirements,
		getPricing: (state) => state.pricing,
		getOrderStatus: (state) => state.orderStatus,
		getConversationId: (state) => state.conversationId,
	},
	mutations: {
		setLoading(state, loading) {
			state.isLoading = loading;
		},
		setError(state, error) {
			state.error = error;
		},
		addMessage(state, message) {
			state.messages.push(message);
		},
		setConversationId(state, id) {
			state.conversationId = id;
		},
		setClientId(state, id) {
			state.clientId = id;
		},
		addRequirement(state, requirement) {
			state.requirements.push(requirement);
		},
		clearRequirements(state) {
			state.requirements = [];
		},
		setPricing(state, pricing) {
			state.pricing = pricing;
		},
		setOrderStatus(state, status) {
			state.orderStatus = status;
		},
		clearMessages(state) {
			state.messages = [];
		},
	},
	actions: {
		// Send message to chatbot
		async sendMessage({ commit, state }, messageText) {
			try {
				commit('setLoading', true);
				commit('setError', null);

				// Add user message to chat
				const userMessage = {
					content: messageText,
					isUser: true,
					timestamp: new Date(),
				};
				commit('addMessage', userMessage);

				// Prepare request data
				const requestData = {
					message: messageText,
					conversation_id: state.conversationId,
					client_id: state.clientId,
				};

				// Send message to API
				const response = await axios.post(`${API_URL}/chat`, requestData);

				// Save conversation ID if not already set
				if (!state.conversationId && response.data.conversation_id) {
					commit('setConversationId', response.data.conversation_id);
				}

				// Add bot response to chat
				const botMessage = {
					content: response.data.message,
					isUser: false,
					timestamp: new Date(),
				};
				commit('addMessage', botMessage);

				// Update requirements if present in response
				if (response.data.requirements) {
					commit('clearRequirements');
					response.data.requirements.forEach((req) => {
						commit('addRequirement', req);
					});
				}

				// Update pricing if present in response
				if (response.data.pricing) {
					commit('setPricing', response.data.pricing);
				}

				return response.data;
			} catch (error) {
				commit('setError', error.response?.data?.detail || 'Error communicating with server');
				return null;
			} finally {
				commit('setLoading', false);
			}
		},

		// Get pricing based on requirements
		async getPricing({ commit, state }) {
			try {
				commit('setLoading', true);
				commit('setError', null);

				// Prepare request data
				const requestData = {
					client_id: state.clientId,
					requirements: state.requirements,
				};

				// Send requirements to API
				const response = await axios.post(`${API_URL}/pricing`, requestData);

				// Update pricing
				commit('setPricing', response.data);

				return response.data;
			} catch (error) {
				commit('setError', error.response?.data?.detail || 'Error calculating pricing');
				return null;
			} finally {
				commit('setLoading', false);
			}
		},

		// Create order inquiry
		async createOrder({ commit, state }) {
			try {
				commit('setLoading', true);
				commit('setError', null);

				// Prepare request data
				const requestData = {
					conversation_id: state.conversationId,
					client_id: state.clientId || 'anonymous',
					requirements: state.requirements,
					price: state.pricing.final_price,
				};

				// Send order request to API
				const response = await axios.post(`${API_URL}/create-order`, requestData);

				// Update order status
				commit('setOrderStatus', response.data);

				return response.data;
			} catch (error) {
				commit('setError', error.response?.data?.detail || 'Error creating order');
				return null;
			} finally {
				commit('setLoading', false);
			}
		},

		// Reset conversation
		resetConversation({ commit }) {
			commit('clearMessages');
			commit('setConversationId', null);
			commit('clearRequirements');
			commit('setPricing', null);
			commit('setOrderStatus', null);
			commit('setError', null);
		},
	},
});
