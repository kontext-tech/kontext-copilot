export class ServiceNotFoundException extends Error {
   constructor(service: string) {
      super(`Requested service ${service} not found`)
      this.name = "ServiceNotFoundException"
   }
}

export class NoInjectionContextFoundException extends Error {
   constructor() {
      super(`No injection context found.`)
      this.name = "NoInjectionContextFoundException"
   }
}

export class LlmProxyServiceRequiredException extends Error {
   constructor() {
      super(`LlmProxyService is required for this operation`)
      this.name = "LlmProxyServiceRequiredException"
   }
}

export class DataProviderServiceRequiredException extends Error {
   constructor() {
      super(`DataProviderService is required for this operation`)
      this.name = "DataProviderServiceRequiredException"
   }
}

export class LlmEndointRequiredException extends Error {
   constructor() {
      super(`LlmService requires an endpoint`)
      this.name = "LlmEndointRequiredException"
   }
}

export class LlmModelRequiredException extends Error {
   constructor() {
      super(`LLM model is required for this operation`)
      this.name = "LlmModelRequiredException"
   }
}

export class NoDoneOrScucessResposneException extends Error {
   constructor() {
      super(`Did not receive done or success response in stream.`)
      this.name = "NoDoneOrScucessResposneException"
   }
}

export class InvalidJsonException extends Error {
   constructor(json: string, error: Error) {
      super(`Invalid JSON: ${json}. Error: ${error.message}`)
      this.name = "InvalidJsonException"
   }
}

export class SessionNotFoundException extends Error {
   constructor() {
      super(`Session not found`)
      this.name = "SessionNotFoundException"
   }
}
