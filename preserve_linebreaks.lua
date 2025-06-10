
-- preserve_linebreaks.lua
-- Filter for better preservation of line breaks and paragraph structure

function LineBreak(el)
    return pandoc.RawInline("latex", "\\\\")
end

function SoftBreak(el)
    return pandoc.RawInline("latex", " ")
end

function Para(el)
    -- Add proper spacing for numbered lists and paragraph breaks
    if #el.content > 0 then
        return pandoc.Para(el.content)
    end
end

-- Improve list formatting
function OrderedList(el)
    -- Ensure proper spacing in numbered lists
    return el
end

function BulletList(el)
    -- Ensure proper spacing in bullet lists
    return el
end
