import Config from '../../core/config'

export default function convertMaskToIndices(
  matchmask = [],
  minMatchCharLength = Config.minMatchCharLength
) {
  let indices = []
  let start = -1
  let end = -1
  let i = 0

  for (let len = matchmask.length; i < len; i += 1) {
    let match = matchmask[i]
    if (match && start === -1) {
      start = i
    } else if (!match && start !== -1) {
      end = i - 1
      if (end - start + 1 >= minMatchCharLength) {
        indices.push([start, end])
      }
      start = -1
    }
  }

  // (i-1 - start) + 1 => i - start
  if (matchmask[i - 1] && i - start >= minMatchCharLength) {
    indices.push([start, i - 1])
  }

  return indices
}
