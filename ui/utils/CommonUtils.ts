import { NoDoneOrScucessResposneException } from "~/types/Errors"
import type { ErrorResponseModel } from "~/types/Schemas"

export const isEmptyOrNull = (str: string | null): boolean => {
   return str === null || str.trim() === ""
}

export const getBaseUrl = (apiBaseUrl: string) => {
   return `${apiBaseUrl}/api`
}

/* Enhanced from https://github.com/ollama/ollama-js/blob/main/src/utils.ts */
export class AbortableAsyncIterator<T extends object> {
   private readonly abortController: AbortController
   private readonly itr: AsyncGenerator<T | ErrorResponseModel>
   private readonly doneCallback: () => void

   constructor(
      abortController: AbortController,
      itr: AsyncGenerator<T | ErrorResponseModel>,
      doneCallback: () => void
   ) {
      this.abortController = abortController
      this.itr = itr
      this.doneCallback = doneCallback
   }

   abort() {
      this.abortController.abort()
   }

   async *[Symbol.asyncIterator]() {
      for await (const message of this.itr) {
         if ("error" in message) {
            throw new Error(message.error)
         }
         yield message

         if (
            ("done" in message && message.done) ||
            ("status" in message && message.status === "success")
         ) {
            this.doneCallback()
            return
         }
      }
      throw new NoDoneOrScucessResposneException()
   }
}

/**
 * Parses a ReadableStream of Uint8Array into JSON objects. https://github.com/ollama/ollama-js/blob/8607c280fa377983d7d9df09fe9fbcaae62a2563/src/utils.ts#L216C1-L244C4
 * @param itr {ReadableStream<Uint8Array>} - The stream to parse
 * @returns {AsyncGenerator<T>} - The parsed JSON objects
 */
export const parseJSON = async function* <T = unknown>(
   itr: ReadableStream<Uint8Array>
): AsyncGenerator<T> {
   const decoder = new TextDecoder("utf-8")
   let buffer = ""

   const reader = itr.getReader()

   while (true) {
      const { done, value: chunk } = await reader.read()

      if (done) {
         break
      }

      buffer += decoder.decode(chunk)

      const parts = buffer.split("\n")

      buffer = parts.pop() ?? ""

      for (const part of parts) {
         try {
            yield JSON.parse(part)
         } catch (error) {
            console.warn("invalid json: ", part)
         }
      }
   }
}
