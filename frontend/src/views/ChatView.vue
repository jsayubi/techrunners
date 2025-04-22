<template>
	<div class="chat-container">
		<div class="chat-header">
			<h2>B2B Sales Support Chat</h2>
			<button @click="resetChat" class="btn btn-secondary btn-sm">New Conversation</button>
		</div>

		<div v-if="error" class="alert alert-error">
			{{ error }}
		</div>

		<div class="chat-messages" ref="messagesContainer">
			<div v-if="messages.length === 0" class="chat-welcome">
				<p>Welcome to our B2B Sales Support Chat!</p>
				<p>How can we help you today?</p>
			</div>

			<div v-for="(message, index) in messages" :key="index" class="message" :class="message.isUser ? 'message-user' : 'message-bot'">
				<div class="message-content">{{ message.content }}</div>
				<div class="message-time">{{ formatTime(message.timestamp) }}</div>
			</div>

			<div v-if="isLoading" class="message message-bot">
				<div class="spinner"></div>
			</div>
		</div>

		<div class="pricing-summary" v-if="pricing">
			<div class="card">
				<div class="card-title">Pricing Summary</div>
				<div class="pricing-details">
					<div class="pricing-row">
						<span>Base Price:</span>
						<span>${{ formatPrice(pricing.base_price) }}</span>
					</div>
					<div v-if="pricing.discount_percentage" class="pricing-row">
						<span>Discount:</span>
						<span>{{ pricing.discount_percentage }}%</span>
					</div>
					<div class="pricing-row pricing-total">
						<span>Final Price:</span>
						<span>${{ formatPrice(pricing.final_price) }}</span>
					</div>
				</div>
				<div class="pricing-actions">
					<button @click="confirmOrder" class="btn">Confirm Order</button>
					<button @click="requestChanges" class="btn btn-secondary">Request Changes</button>
				</div>
			</div>
		</div>

		<div class="order-confirmation" v-if="orderStatus">
			<div class="card">
				<div class="card-title">Order Inquiry Created</div>
				<p>Your order inquiry has been created successfully.</p>
				<p>
					Order Reference: <strong>{{ orderStatus.order_id }}</strong>
				</p>
				<p>A sales representative will contact you shortly.</p>
			</div>
		</div>

		<div class="chat-input">
			<form @submit.prevent="submitMessage">
				<div class="input-group">
					<input type="text" v-model="messageInput" placeholder="Type your message here..." :disabled="isLoading || !!orderStatus" class="form-input" />
					<button type="submit" class="btn" :disabled="isLoading || !messageInput.trim() || !!orderStatus">
						<span v-if="!isLoading">Send</span>
						<span v-else class="spinner"></span>
					</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';

export default {
	name: 'ChatView',
	data() {
		return {
			messageInput: '',
		};
	},
	computed: {
		...mapGetters(['getMessages', 'isLoading', 'getError', 'getRequirements', 'getPricing', 'getOrderStatus']),
		messages() {
			return this.getMessages;
		},
		error() {
			return this.getError;
		},
		requirements() {
			return this.getRequirements;
		},
		pricing() {
			return this.getPricing;
		},
		orderStatus() {
			return this.getOrderStatus;
		},
	},
	methods: {
		...mapActions(['sendMessage', 'getPricing', 'createOrder', 'resetConversation']),
		...mapMutations(['setError']),
		async submitMessage() {
			if (!this.messageInput.trim() || this.isLoading) return;

			const messageText = this.messageInput;
			this.messageInput = '';

			await this.sendMessage(messageText);
			this.scrollToBottom();
		},
		formatTime(date) {
			if (!date) return '';
			const d = new Date(date);
			return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
		},
		formatPrice(price) {
			return price.toLocaleString('en-US', {
				minimumFractionDigits: 2,
				maximumFractionDigits: 2,
			});
		},
		scrollToBottom() {
			setTimeout(() => {
				if (this.$refs.messagesContainer) {
					this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
				}
			}, 100);
		},
		async confirmOrder() {
			try {
				await this.createOrder();
				this.scrollToBottom();
			} catch (error) {
				this.setError('Failed to create order. Please try again.');
			}
		},
		requestChanges() {
			this.messageInput = 'I need to make some changes to this quote.';
		},
		resetChat() {
			this.resetConversation();
			this.messageInput = '';
		},
	},
	mounted() {
		this.scrollToBottom();
	},
	updated() {
		this.scrollToBottom();
	},
};
</script>

<style scoped>
.chat-container {
	max-width: 800px;
	margin: 0 auto;
	height: 100%;
	display: flex;
	flex-direction: column;
}

.chat-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 1rem;
}

.chat-header h2 {
	color: var(--primary-color);
	font-size: 1.5rem;
	margin: 0;
}

.btn-sm {
	padding: 0.25rem 0.5rem;
	font-size: 0.75rem;
}

.chat-messages {
	flex-grow: 1;
	overflow-y: auto;
	padding: 1rem;
	background-color: #f8fafc;
	border-radius: 0.5rem;
	border: 1px solid var(--border-color);
	margin-bottom: 1rem;
	height: 400px;
	display: flex;
	flex-direction: column;
}

.chat-welcome {
	text-align: center;
	color: #64748b;
	margin: auto 0;
}

.chat-welcome p {
	margin-bottom: 0.5rem;
}

.message {
	position: relative;
	margin-bottom: 1rem;
}

.message-content {
	margin-bottom: 0.25rem;
}

.message-time {
	font-size: 0.7rem;
	opacity: 0.7;
	text-align: right;
}

.pricing-summary {
	margin-bottom: 1rem;
}

.pricing-details {
	margin-bottom: 1rem;
}

.pricing-row {
	display: flex;
	justify-content: space-between;
	margin-bottom: 0.5rem;
}

.pricing-total {
	font-weight: bold;
	border-top: 1px solid var(--border-color);
	padding-top: 0.5rem;
}

.pricing-actions {
	display: flex;
	gap: 0.5rem;
}

.order-confirmation {
	margin-bottom: 1rem;
}

.chat-input {
	margin-bottom: 1rem;
}

.input-group {
	display: flex;
}

.input-group .form-input {
	flex: 1;
	border-top-right-radius: 0;
	border-bottom-right-radius: 0;
}

.input-group .btn {
	border-top-left-radius: 0;
	border-bottom-left-radius: 0;
}

@media (max-width: 600px) {
	.chat-container {
		padding: 0 1rem;
	}

	.chat-messages {
		height: 350px;
	}
}
</style>
