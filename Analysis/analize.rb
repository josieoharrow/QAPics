require 'chunky_png'


if (ARGV[0] == nil || ARGV[1] == nil) 
	p 'invalid parameters'
	return
end

image1 = ChunkyPNG::Image.from_file(ARGV[0])
image2 = ChunkyPNG::Image.from_file(ARGV[1])

png_stream_1 = ChunkyPNG::Datastream.from_file(ARGV[0])
png_stream_1.each_chunk { |chunk| 
begin
	color = ChunkyPNG::Palette[40] 
 	p color
rescue
	p ' here'
end
}
