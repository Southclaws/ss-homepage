build:
	docker build \
		-t southclaws/tw-homepage:latest \
		.

run:
	-docker rm tw-homepage
	docker run \
		--name tw-homepage \
		--publish 8080:80 \
		southclaws/tw-homepage:latest
