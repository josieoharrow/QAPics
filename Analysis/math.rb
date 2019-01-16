require 'prime'

i = 0
j = 0

while i<4
	if Prime.prime?(2**j + 1)
		i = i+1
		puts 2**j + 1
		puts "ELEMENT: " + j.to_s
	end
	j = j + 1
end
