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

export { ServiceNotFoundException, NoInjectionContextFoundException }
