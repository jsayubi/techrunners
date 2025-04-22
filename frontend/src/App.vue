<template>
	<div class="app-container">
		<header class="app-header">
			<div class="logo">
				<h1>B2B Sales Support</h1>
			</div>
		</header>
		<main class="app-content">
			<router-view />
		</main>
		<footer class="app-footer">
			<p>&copy; 2024 B2B Sales Support Chatbot</p>
		</footer>
	</div>
</template>

<script>
export default {
	name: 'App',
};
</script>

<style>
:root {
	--primary-color: #4f46e5;
	--primary-hover: #4338ca;
	--secondary-color: #22d3ee;
	--text-color: #1e293b;
	--light-color: #f8fafc;
	--border-color: #e2e8f0;
	--success-color: #10b981;
	--error-color: #ef4444;
	--warning-color: #f59e0b;
}

* {
	box-sizing: border-box;
	margin: 0;
	padding: 0;
}

body {
	font-family: 'Roboto', sans-serif;
	color: var(--text-color);
	line-height: 1.6;
	background-color: var(--light-color);
}

.app-container {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
}

.app-header {
	background-color: white;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
	padding: 1rem 2rem;
}

.app-header .logo h1 {
	color: var(--primary-color);
	font-size: 1.5rem;
	font-weight: 700;
}

.app-content {
	flex: 1;
	padding: 2rem;
}

.app-footer {
	background-color: white;
	padding: 1rem 2rem;
	text-align: center;
	border-top: 1px solid var(--border-color);
	font-size: 0.875rem;
	color: #64748b;
}

a {
	color: var(--primary-color);
	text-decoration: none;
}

a:hover {
	color: var(--primary-hover);
}

.btn {
	display: inline-block;
	background-color: var(--primary-color);
	color: white;
	padding: 0.5rem 1rem;
	border-radius: 0.375rem;
	border: none;
	cursor: pointer;
	font-size: 0.875rem;
	font-weight: 500;
	transition: background-color 0.2s;
}

.btn:hover {
	background-color: var(--primary-hover);
}

.btn-secondary {
	background-color: var(--secondary-color);
}

.container {
	max-width: 1200px;
	margin: 0 auto;
	padding: 0 1rem;
}
</style>
