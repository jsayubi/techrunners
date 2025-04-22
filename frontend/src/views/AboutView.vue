<template>
	<div class="about-container">
		<div class="card">
			<h1 class="card-title">About B2B Sales Support Chatbot</h1>

			<div class="about-section">
				<h2>Our AI-Powered Sales Support</h2>
				<p>
					The B2B Sales Support Chatbot is designed to streamline your sales inquiries and provide instant support for your business needs. Our AI-powered system can help you with product information, gather your requirements, and generate customized pricing based on your specific business needs.
				</p>
			</div>

			<div class="about-section">
				<h2>Key Features</h2>
				<ul>
					<li><strong>Smart Greetings:</strong> Instant, friendly welcome in your preferred language.</li>
					<li><strong>Product Expertise:</strong> Answers detailed product questions with up‑to‑date information.</li>
					<li><strong>Requirements Gathering:</strong> Clarifies what features you need and what's optional.</li>
					<li><strong>Dynamic Pricing:</strong> Provides transparent, fair pricing based on your requirements.</li>
					<li><strong>Seamless Handoff:</strong> Connect with a human sales representative when needed.</li>
					<li><strong>Multilingual Support:</strong> Communicate in your preferred language.</li>
				</ul>
			</div>

			<div class="about-section">
				<h2>How It Works</h2>
				<ol>
					<li>Start a conversation with our chatbot</li>
					<li>Describe your business needs and ask questions about our products</li>
					<li>The chatbot will gather your requirements</li>
					<li>Receive a customized pricing proposal</li>
					<li>Confirm the order or request changes</li>
					<li>Get connected with a human sales representative if needed</li>
				</ol>
			</div>

			<div class="about-section">
				<h2>Get Started</h2>
				<p>Ready to experience our AI-powered sales support? Head back to the chat and start a conversation with our chatbot.</p>
				<router-link to="/" class="btn">Go to Chat</router-link>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'AboutView',
};
</script>

<style scoped>
.about-container {
	max-width: 800px;
	margin: 0 auto;
	padding: 0 1rem;
}

.about-section {
	margin-bottom: 2rem;
}

.about-section h2 {
	color: var(--primary-color);
	font-size: 1.25rem;
	margin-bottom: 1rem;
}

.about-section p {
	margin-bottom: 1rem;
	line-height: 1.6;
}

ul,
ol {
	margin-left: 1.5rem;
	margin-bottom: 1rem;
}

li {
	margin-bottom: 0.5rem;
}

.btn {
	display: inline-block;
	margin-top: 1rem;
}
</style>
