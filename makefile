build:
	docker build \
		-t southclaws/ss-homepage:latest \
		.

run:
	-docker rm ss-homepage
	docker run \
		--name ss-homepage \
		--publish 8080:80 \
		southclaws/ss-homepage:latest
