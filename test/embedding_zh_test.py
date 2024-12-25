from transformers import AutoModel
from numpy.linalg import norm

model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-code', trust_remote_code=True)

if __name__ == '__main__':
    code = """
    public static final RetryTemplate DEFAULT_RETRY_TEMPLATE = RetryTemplate.builder()
		.maxAttempts(10)
		.retryOn(TransientAiException.class)
		.exponentialBackoff(Duration.ofMillis(2000), 5, Duration.ofMillis(3 * 60000))
		.withListener(new RetryListener() {
			@Override
			public <T extends Object, E extends Throwable> void onError(RetryContext context,
					RetryCallback<T, E> callback, Throwable throwable) {
				logger.warn("Retry error. Retry count:" + context.getRetryCount(), throwable);
			};
		})
		.build();

	public static final ResponseErrorHandler DEFAULT_RESPONSE_ERROR_HANDLER = new ResponseErrorHandler() {

		@Override
		public boolean hasError(@NonNull ClientHttpResponse response) throws IOException {
			return response.getStatusCode().isError();
		}

		@Override
		public void handleError(@NonNull ClientHttpResponse response) throws IOException {
			if (response.getStatusCode().isError()) {
				String error = StreamUtils.copyToString(response.getBody(), StandardCharsets.UTF_8);
				String message = String.format("%s - %s", response.getStatusCode().value(), error);
				/**
				 * Thrown on 4xx client errors, such as 401 - Incorrect API key provided,
				 * 401 - You must be a member of an organization to use the API, 429 -
				 * Rate limit reached for requests, 429 - You exceeded your current quota
				 * , please check your plan and billing details.
				 */
				if (response.getStatusCode().is4xxClientError()) {
					throw new NonTransientAiException(message);
				}
				throw new TransientAiException(message);
			}
		}
	};
    """

    question = "what is the default retry template in spring framework?"

    embeddings = model.encode([code, question])
    cos_sim = lambda a, b: (a @ b.T) / (norm(a) * norm(b))
    print(f"Similarity: {cos_sim(embeddings[0], embeddings[1])}")
