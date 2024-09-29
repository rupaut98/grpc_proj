PROTO_DIR = src/protos
GEN_DIR = src/generated

all: generate_protos

generate_protos:
	@mkdir -p $(GEN_DIR)
	python -m grpc_tools.protoc -I=$(PROTO_DIR) --python_out=$(GEN_DIR) --grpc_python_out=$(GEN_DIR) $(PROTO_DIR)/*.proto

clean:
	rm -rf $(GEN_DIR)/*.py
