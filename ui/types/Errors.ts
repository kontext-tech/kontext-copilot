class ServiceNotFoundException extends Error {
   constructor(service: string) {
      super(`Requested service ${service} not found`)
      this.name = "ServiceNotFoundException"
   }
}

class NoInjectionContextFoundException extends Error {
   constructor() {
      super(`No injection context found.`)
      this.name = "NoInjectionContextFoundException"
   }
}

class LlmProxyServiceRequiredException extends Error {
   constructor() {
      super(`LlmProxyService is required for this operation`)
      this.name = "LlmProxyServiceRequiredException"
   }
}

class LlmEndointRequiredException extends Error {
   constructor() {
      super(`LlmService requires an endpoint`)
      this.name = "LlmEndointRequiredException"
   }
}

class LlmModelRequiredException extends Error {
   constructor() {
      super(`LLM model is required for this operation`)
      this.name = "LlmModelRequiredException"
   }
}

export {
   ServiceNotFoundException,
   NoInjectionContextFoundException,
   LlmProxyServiceRequiredException,
   LlmEndointRequiredException,
   LlmModelRequiredException
}
