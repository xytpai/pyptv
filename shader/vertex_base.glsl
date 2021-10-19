#version 330 core
layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_normal;

out vec3 fragpos;
out vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
	fragpos = vec3(model * vec4(in_position, 1.0));
	normal = mat3(transpose(inverse(model))) * in_normal;
	gl_Position = projection * view * model * vec4(in_position, 1.0f);
}