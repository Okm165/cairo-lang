import json


class Felt:
    def __init__(self, cairo_obj) -> None:
        self.value = int(cairo_obj)

    def __repr__(self) -> str:
        return f"{hex(self.value)}"


class FeltArray:
    def __init__(self, memory, cairo_ptr, len) -> None:
        self.value = [Felt(memory[cairo_ptr + i]) for i in range(len)]

    def __repr__(self) -> str:
        return f"{self.value}"


class SegmentInfo:
    def __init__(self, cairo_obj) -> None:
        self.begin_addr = Felt(cairo_obj.begin_addr)
        self.stop_ptr = Felt(cairo_obj.stop_ptr)

    def __repr__(self) -> str:
        dict = {
            "begin_addr": self.begin_addr,
            "stop_ptr": self.stop_ptr,
        }
        return f"{dict}"


class AddrValue:
    def __init__(self, cairo_obj) -> None:
        self.address = Felt(cairo_obj.address)
        self.value = Felt(cairo_obj.value)

    def __repr__(self) -> str:
        dict = {
            "address": self.address,
            "value": self.value,
        }
        return f"{dict}"


class ContinuousPageHeader:
    def __init__(self, cairo_obj) -> None:
        self.start_address = Felt(cairo_obj.start_address)
        self.size = Felt(cairo_obj.size)
        self.hash = Felt(cairo_obj.hash)
        self.prod = Felt(cairo_obj.prod)

    def __repr__(self) -> str:
        dict = {
            "start_address": self.start_address,
            "size": self.size,
            "hash": self.hash,
            "prod": self.prod,
        }
        return f"{dict}"


class ChannelUnsentFelt:
    def __init__(self, cairo_obj) -> None:
        self.value = Felt(cairo_obj.value)

    def __repr__(self) -> str:
        dict = {
            "value": self.value,
        }
        return f"{dict}"


class ChannelSentFelt:
    def __init__(self, cairo_obj) -> None:
        self.value = Felt(cairo_obj.value)

    def __repr__(self) -> str:
        dict = {
            "value": self.value,
        }
        return f"{dict}"


class StarkUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.traces = TracesUnsentCommitment(cairo_obj.traces)
        self.composition = TableUnsentCommitment(cairo_obj.composition)
        self.oods_values = self.init_oods_values(cairo_obj.oods_values, 10)
        self.fri = FriUnsentCommitment(cairo_obj.fri)
        self.proof_of_work = ProofOfWorkUnsentCommitment(cairo_obj.proof_of_work)

    def __repr__(self) -> str:
        dict = {
            "traces": self.traces,
            "composition": self.composition,
            "oods_values": self.oods_values,
            "fri": self.fri,
            "proof_of_work": self.proof_of_work,
        }
        return f"{dict}"

    # n_oods_values := air.mask_size + air.constraint_degree.
    def init_oods_values(self, cairo_obj, n_oods_values) -> list[ChannelUnsentFelt]:
        res = []
        for i in range(n_oods_values):
            res.append(ChannelUnsentFelt(cairo_obj[i]))
        return res


class StarkCommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.traces = TracesCommitment(memory, cairo_obj.traces)
        self.composition = TableCommitment(cairo_obj.composition)
        self.interaction_after_composition = InteractionValuesAfterComposition(
            cairo_obj.interaction_after_composition
        )
        self.oods_values = self.init_oods_values(cairo_obj.oods_values)
        self.interaction_after_oods = InteractionValuesAfterOods(
            cairo_obj.interaction_after_oods
        )
        self.fri = FriCommitment(cairo_obj.fri)

    def __repr__(self) -> str:
        dict = {
            "traces": self.traces,
            "composition": self.composition,
            "interaction_after_composition": self.interaction_after_composition,
            "oods_values": self.oods_values,
            "interaction_after_oods": self.interaction_after_oods,
            "fri": self.fri,
        }
        return f"{dict}"

    # n_oods_values := air.mask_size + air.constraint_degree.
    def init_oods_values(self, cairo_obj, n_oods_values) -> list[ChannelSentFelt]:
        res = []
        for i in range(n_oods_values):
            res.append(ChannelSentFelt(cairo_obj[i]))
        return res


class InteractionValuesAfterComposition:
    def __init__(self, cairo_obj) -> None:
        self.oods_point = Felt(cairo_obj.oods_point)

    def __repr__(self) -> str:
        dict = {
            "oods_point": self.oods_point,
        }
        return f"{dict}"


class InteractionValuesAfterOods:
    def __init__(self, memory, cairo_obj, n_oods_values) -> None:
        self.coefficients = FeltArray(memory, cairo_obj.coefficients, n_oods_values)

    def __repr__(self) -> str:
        dict = {
            "coefficients": self.coefficients,
        }
        return f"{dict}"


class StarkWitness:
    def __init__(self, memory, cairo_obj, n_layers) -> None:
        # self.traces_decommitment = TracesDecommitment(
        #     memory, cairo_obj.traces_decommitment
        # )
        # self.traces_witness = TracesWitness(cairo_obj.traces_witness)
        self.composition_decommitment = TableDecommitment(
            memory, cairo_obj.composition_decommitment
        )
        self.composition_witness = TableCommitmentWitness(
            memory, cairo_obj.composition_witness
        )
        # self.fri_witness = FriWitness(memory, cairo_obj.fri_witness, n_layers)

    def __repr__(self) -> str:
        dict = {
            "traces_decommitment": self.traces_decommitment,
            "traces_witness": self.traces_witness,
            "composition_decommitment": self.composition_decommitment,
            "composition_witness": self.composition_witness,
            "fri_witness": self.fri_witness,
        }
        return f"{dict}"


class StarkWitness:
    def __init__(self, cairo_obj) -> None:
        self.config = StarkConfig(cairo_obj.config)
        self.public_input = PublicInput(cairo_obj.public_input)
        self.unsent_commitment = StarkUnsentCommitment(cairo_obj.unsent_commitment)
        self.witness = StarkUnsentCommitment(cairo_obj.witness)

    def __repr__(self) -> str:
        dict = {
            "config": self.config,
            "public_input": self.public_input,
            "unsent_commitment": self.unsent_commitment,
            "witness": self.witness,
        }
        return f"{dict}"


class StarkConfig:
    def __init__(self, cairo_obj) -> None:
        self.traces = TracesConfig(cairo_obj.traces)
        self.composition = TableCommitmentConfig(cairo_obj.composition)
        self.fri = FriConfig(cairo_obj.fri)
        self.proof_of_work = ProofOfWorkConfig(cairo_obj.proof_of_work)
        self.log_trace_domain_size = Felt(cairo_obj.log_trace_domain_size)
        self.n_queries = Felt(cairo_obj.n_queries)
        self.log_n_cosets = Felt(cairo_obj.log_n_cosets)
        self.n_verifier_friendly_commitment_layers = Felt(
            cairo_obj.n_verifier_friendly_commitment_layers
        )

    def __repr__(self) -> str:
        dict = {
            "traces": self.traces,
            "composition": self.composition,
            "fri": self.fri,
            "proof_of_work": self.proof_of_work,
            "log_trace_domain_size": self.log_trace_domain_size,
            "n_queries": self.n_queries,
            "log_n_cosets": self.log_n_cosets,
            "n_verifier_friendly_commitment_layers": self.n_verifier_friendly_commitment_layers,
        }
        return f"{dict}"


class TracesUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.original = TableUnsentCommitment(cairo_obj.original)
        self.interaction = TableUnsentCommitment(cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "original": self.original,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TracesCommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.public_input = PublicInput(memory, cairo_obj.public_input)
        self.original = TableCommitment(cairo_obj.original)
        self.interaction_elements = FeltArray(memory, cairo_obj.interaction_elements, 6)
        self.interaction = TableCommitment(cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "public_input": self.public_input,
            "original": self.original,
            "interaction_elements": self.interaction_elements,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TracesDecommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.original = TableDecommitment(memory, cairo_obj.original)
        self.interaction = TableDecommitment(memory, cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "original": self.original,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TracesWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.original = TableCommitmentWitness(memory, cairo_obj.original)
        self.interaction = TableCommitmentWitness(memory, cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "original": self.original,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TracesConfig:
    def __init__(self, cairo_obj) -> None:
        self.original = TableCommitmentConfig(cairo_obj.original)
        self.interaction = TableCommitmentConfig(cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "original": self.original,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TableUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.vector = VectorUnsentCommitment(cairo_obj.vector)

    def __repr__(self) -> str:
        dict = {
            "vector": self.vector,
        }
        return f"{dict}"


class TableCommitment:
    def __init__(self, cairo_obj) -> None:
        self.config = TableCommitmentConfig(cairo_obj.config)
        self.vector_commitment = VectorCommitment(cairo_obj.vector_commitment)

    def __repr__(self) -> str:
        dict = {
            "config": self.config,
            "vector_commitment": self.vector_commitment,
        }
        return f"{dict}"


class TableCommitmentConfig:
    def __init__(self, cairo_obj) -> None:
        self.n_columns = Felt(cairo_obj.n_columns)
        self.vector = VectorCommitmentConfig(cairo_obj.vector)

    def __repr__(self) -> str:
        dict = {
            "n_columns": self.n_columns,
            "vector": self.vector,
        }
        return f"{dict}"


class TableDecommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.n_values = Felt(cairo_obj.n_values)
        self.values = FeltArray(memory, cairo_obj.values, self.n_values.value)

    def __repr__(self) -> str:
        dict = {
            "n_values": self.n_values,
            "values": self.values,
        }
        return f"{dict}"


class TableCommitmentWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.vector = VectorCommitmentWitness(memory, cairo_obj.vector)

    def __repr__(self) -> str:
        dict = {
            "vector": self.vector,
        }
        return f"{dict}"


class VectorUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.commitment_hash = ChannelSentFelt(cairo_obj.commitment_hash)

    def __repr__(self) -> str:
        dict = {
            "commitment_hash": self.commitment_hash,
        }
        return f"{dict}"


class VectorCommitment:
    def __init__(self, cairo_obj) -> None:
        self.config = VectorCommitmentConfig(cairo_obj.config)
        self.commitment_hash = ChannelSentFelt(cairo_obj.commitment_hash)

    def __repr__(self) -> str:
        dict = {
            "config": self.config,
        }
        return f"{dict}"


class VectorCommitmentConfig:
    def __init__(self, cairo_obj) -> None:
        self.height = Felt(cairo_obj.height)
        self.n_verifier_friendly_commitment_layers = Felt(
            cairo_obj.n_verifier_friendly_commitment_layers
        )

    def __repr__(self) -> str:
        dict = {
            "height": self.height,
            "n_verifier_friendly_commitment_layers": self.n_verifier_friendly_commitment_layers,
        }
        return f"{dict}"


class VectorCommitmentWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.n_authentications = Felt(cairo_obj.n_authentications)
        self.authentications = FeltArray(
            memory, cairo_obj.authentications, self.n_authentications.value
        )

    def __repr__(self) -> str:
        dict = {
            "n_authentications": self.n_authentications,
            "authentications": self.authentications,
        }
        return f"{dict}"


class VectorQuery:
    def __init__(self, cairo_obj) -> None:
        self.index = Felt(cairo_obj.index)
        self.value = Felt(cairo_obj.value)

    def __repr__(self) -> str:
        dict = {
            "index": self.index,
            "value": self.value,
        }
        return f"{dict}"


class VectorQueryWithDepth:
    def __init__(self, cairo_obj) -> None:
        self.index = Felt(cairo_obj.index)
        self.value = Felt(cairo_obj.value)
        self.depth = Felt(cairo_obj.depth)

    def __repr__(self) -> str:
        dict = {
            "index": self.index,
            "value": self.value,
            "depth": self.depth,
        }
        return f"{dict}"


class ProofOfWorkConfig:
    def __init__(self, cairo_obj) -> None:
        self.n_bits = Felt(cairo_obj.n_bits)

    def __repr__(self) -> str:
        dict = {
            "n_bits": self.n_bits,
        }
        return f"{dict}"


class ProofOfWorkUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.nonce = ChannelUnsentFelt(cairo_obj.nonce)

    def __repr__(self) -> str:
        dict = {
            "nonce": self.nonce,
        }
        return f"{dict}"


class StarkDomains:
    def __init__(self, cairo_obj) -> None:
        self.log_eval_domain_size = Felt(cairo_obj.log_eval_domain_size)
        self.eval_domain_size = Felt(cairo_obj.eval_domain_size)
        self.eval_generator = Felt(cairo_obj.eval_generator)
        self.log_trace_domain_size = Felt(cairo_obj.log_trace_domain_size)
        self.trace_domain_size = Felt(cairo_obj.trace_domain_size)
        self.trace_generator = Felt(cairo_obj.trace_generator)

    def __repr__(self) -> str:
        dict = {
            "log_eval_domain_size": self.log_eval_domain_size,
            "eval_domain_size": self.eval_domain_size,
            "eval_generator": self.eval_generator,
            "log_trace_domain_size": self.log_trace_domain_size,
            "trace_domain_size": self.trace_domain_size,
            "trace_generator": self.trace_generator,
        }
        return f"{dict}"


class FriUnsentCommitment:
    def __init__(self, cairo_obj, n_layers, log_last_layer_degree_bound) -> None:
        self.inner_layers = TableUnsentCommitment(cairo_obj.inner_layers, n_layers - 1)
        self.last_layer_coefficients = FeltArray(
            cairo_obj.last_layer_coefficients, 2**log_last_layer_degree_bound
        )

    def __repr__(self) -> str:
        dict = {
            "inner_layers": self.inner_layers,
            "last_layer_coefficients": self.last_layer_coefficients,
        }
        return f"{dict}"

    def init_inner_layers(self, cairo_obj, len) -> list[TableUnsentCommitment]:
        return [TableUnsentCommitment(cairo_obj[i]) for i in range(len)]

    def init_last_layer_coefficients(self, cairo_obj, len) -> list[ChannelUnsentFelt]:
        return [ChannelUnsentFelt(cairo_obj[i]) for i in range(len)]


class FriCommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.config = FriConfig(memory, cairo_obj.config)
        # self.inner_layers = self.init_inner_layers(
        #     cairo_obj.inner_layers, self.config.n_layers.value - 1
        # )
        self.eval_points = FeltArray(
            memory, cairo_obj.eval_points, self.config.n_layers.value
        )
        self.last_layer_coefficients = self.init_last_layer_coefficients(
            cairo_obj.last_layer_coefficients,
            2**self.config.log_last_layer_degree_bound.value,
        )

    def __repr__(self) -> str:
        dict = {
            "config": self.config,
            # "inner_layers": self.inner_layers,
            "eval_points": self.eval_points,
            "last_layer_coefficients": self.last_layer_coefficients,
        }
        return f"{dict}"

    def init_inner_layers(self, cairo_obj, len) -> list[TableCommitment]:
        return [TableCommitment(cairo_obj[i]) for i in range(len)]

    def init_last_layer_coefficients(self, cairo_obj, len) -> list[ChannelSentFelt]:
        return [ChannelSentFelt(cairo_obj[i]) for i in range(len)]


class FriDecommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.n_values = Felt(cairo_obj.n_values)
        self.values = FeltArray(memory, cairo_obj.values, self.n_values.value)
        self.points = FeltArray(memory, cairo_obj.points, self.n_values.value)

    def __repr__(self) -> str:
        dict = {
            "n_values": self.n_values,
            "values": self.values,
            "points": self.points,
        }
        return f"{dict}"


class FriLayerWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.n_leaves = Felt(cairo_obj.n_leaves)
        self.leaves = FeltArray(memory, cairo_obj.leaves, self.n_leaves.value)
        self.table_witness = TableCommitmentWitness(memory, cairo_obj.table_witness)

    def __repr__(self) -> str:
        dict = {
            "n_leaves": self.n_leaves,
            "leaves": self.leaves,
            "table_witness": self.table_witness,
        }
        return f"{dict}"


class FriWitness:
    def __init__(self, memory, cairo_obj, n_layers) -> None:
        self.layers = self.init_layers(memory, cairo_obj.layers, n_layers.value - 1)

    def __repr__(self) -> str:
        dict = {
            "layers": self.layers,
        }
        return f"{dict}"

    def init_layers(self, memory, cairo_obj, len) -> list[FriLayerWitness]:
        return [FriLayerWitness(memory, cairo_obj[i]) for i in range(len)]


class FriConfig:
    def __init__(self, memory, cairo_obj) -> None:
        self.log_input_size = Felt(cairo_obj.log_input_size)
        self.n_layers = Felt(cairo_obj.n_layers)
        self.inner_layers = self.init_inner_layers(
            cairo_obj.inner_layers, self.n_layers.value - 1
        )
        self.fri_step_sizes = FeltArray(
            memory, cairo_obj.fri_step_sizes, self.n_layers.value
        )
        self.log_last_layer_degree_bound = Felt(cairo_obj.log_last_layer_degree_bound)

    def __repr__(self) -> str:
        dict = {
            "log_input_size": self.log_input_size,
            "n_layers": self.n_layers,
            "inner_layers": self.inner_layers,
            "fri_step_sizes": self.fri_step_sizes,
            "log_last_layer_degree_bound": self.log_last_layer_degree_bound,
        }
        return f"{dict}"

    def init_inner_layers(self, cairo_obj, len) -> list[TableCommitmentConfig]:
        return [TableCommitmentConfig(cairo_obj[i]) for i in range(len)]


class PublicInput:
    def __init__(self, memory, cairo_obj) -> None:
        self.log_n_steps = Felt(cairo_obj.log_n_steps)
        self.range_check_min = Felt(cairo_obj.range_check_min)
        self.range_check_max = Felt(cairo_obj.range_check_max)
        self.layout = Felt(cairo_obj.layout)
        self.dynamic_params = FeltArray(memory, cairo_obj.dynamic_params, 0)
        self.n_segments = Felt(cairo_obj.n_segments)
        self.segments = self.init_segments(cairo_obj.segments, self.n_segments.value)
        self.padding_addr = Felt(cairo_obj.padding_addr)
        self.padding_value = Felt(cairo_obj.padding_value)
        self.main_page_len = Felt(cairo_obj.main_page_len)
        self.main_page = self.init_main_page(
            cairo_obj.main_page, self.main_page_len.value
        )
        self.n_continuous_pages = Felt(cairo_obj.n_continuous_pages)
        self.continuous_page_headers = self.init_continuous_page_headers(
            cairo_obj.continuous_page_headers, self.n_continuous_pages.value
        )

    def __repr__(self) -> str:
        dict = {
            "log_n_steps": self.log_n_steps,
            "range_check_min": self.range_check_min,
            "range_check_max": self.range_check_max,
            "layout": self.layout,
            "dynamic_params": self.dynamic_params,
            "n_segments": self.n_segments,
            "segments": self.segments,
            "padding_addr": self.padding_addr,
            "padding_value": self.padding_value,
            "main_page_len": self.main_page_len,
            "main_page": self.main_page,
            "n_continuous_pages": self.n_continuous_pages,
            "continuous_page_headers": self.continuous_page_headers,
        }
        return f"{dict}"

    def init_segments(self, cairo_obj, len) -> list[SegmentInfo]:
        return [SegmentInfo(cairo_obj[i]) for i in range(len)]

    def init_main_page(self, cairo_obj, len) -> list[AddrValue]:
        return [AddrValue(cairo_obj[i]) for i in range(len)]

    def init_continuous_page_headers(
        self, cairo_obj, len
    ) -> list[ContinuousPageHeader]:
        return [ContinuousPageHeader(cairo_obj[i]) for i in range(len)]


class Channel:
    def __init__(self, cairo_obj) -> None:
        self.digest = Felt(cairo_obj.digest)
        self.counter = Felt(cairo_obj.counter)

    def __repr__(self) -> str:
        dict = {
            "digest": self.digest,
            "counter": self.counter,
        }
        return f"{dict}"


class EcPoint:
    def __init__(self, cairo_obj) -> None:
        self.x = Felt(cairo_obj.x)
        self.y = Felt(cairo_obj.y)

    def __repr__(self) -> str:
        dict = {
            "x": self.x,
            "y": self.y,
        }
        return f"{dict}"


class CurveConfig:
    def __init__(self, cairo_obj) -> None:
        self.alpha = Felt(cairo_obj.alpha)
        self.beta = Felt(cairo_obj.beta)

    def __repr__(self) -> str:
        dict = {
            "alpha": self.alpha,
            "beta": self.beta,
        }
        return f"{dict}"


class EcdsaSigConfig:
    def __init__(self, cairo_obj) -> None:
        self.alpha = Felt(cairo_obj.alpha)
        self.beta = Felt(cairo_obj.beta)
        self.shift_point = EcPoint(cairo_obj.shift_point)

    def __repr__(self) -> str:
        dict = {
            "alpha": self.alpha,
            "beta": self.beta,
            "shift_point": self.shift_point,
        }
        return f"{dict}"


class GlobalValues:
    def __init__(self, cairo_obj) -> None:
        self.trace_length = Felt(cairo_obj.trace_length)
        self.initial_pc = Felt(cairo_obj.initial_pc)
        self.final_pc = Felt(cairo_obj.final_pc)
        self.initial_ap = Felt(cairo_obj.initial_ap)
        self.final_ap = Felt(cairo_obj.final_ap)
        self.initial_pedersen_addr = Felt(cairo_obj.initial_pedersen_addr)
        self.initial_range_check_addr = Felt(cairo_obj.initial_range_check_addr)
        self.initial_ecdsa_addr = Felt(cairo_obj.initial_ecdsa_addr)
        self.initial_bitwise_addr = Felt(cairo_obj.initial_bitwise_addr)
        self.initial_ec_op_addr = Felt(cairo_obj.initial_ec_op_addr)
        self.initial_keccak_addr = Felt(cairo_obj.initial_keccak_addr)
        self.initial_poseidon_addr = Felt(cairo_obj.initial_poseidon_addr)
        self.range_check_min = Felt(cairo_obj.range_check_min)
        self.range_check_max = Felt(cairo_obj.range_check_max)
        self.offset_size = Felt(cairo_obj.offset_size)
        self.half_offset_size = Felt(cairo_obj.half_offset_size)
        self.pedersen__shift_point = EcPoint(cairo_obj.pedersen__shift_point)
        self.ecdsa__sig_config = EcdsaSigConfig(cairo_obj.ecdsa__sig_config)
        self.ec_op__curve_config = CurveConfig(cairo_obj.ec_op__curve_config)
        self.pedersen__points__x = Felt(cairo_obj.pedersen__points__x)
        self.pedersen__points__y = Felt(cairo_obj.pedersen__points__y)
        self.ecdsa__generator_points__x = Felt(cairo_obj.ecdsa__generator_points__x)
        self.ecdsa__generator_points__y = Felt(cairo_obj.ecdsa__generator_points__y)
        self.keccak__keccak__keccak_round_key0 = Felt(
            cairo_obj.keccak__keccak__keccak_round_key0
        )
        self.keccak__keccak__keccak_round_key1 = Felt(
            cairo_obj.keccak__keccak__keccak_round_key1
        )
        self.keccak__keccak__keccak_round_key3 = Felt(
            cairo_obj.keccak__keccak__keccak_round_key3
        )
        self.keccak__keccak__keccak_round_key7 = Felt(
            cairo_obj.keccak__keccak__keccak_round_key7
        )
        self.keccak__keccak__keccak_round_key15 = Felt(
            cairo_obj.keccak__keccak__keccak_round_key15
        )
        self.keccak__keccak__keccak_round_key31 = Felt(
            cairo_obj.keccak__keccak__keccak_round_key31
        )
        self.keccak__keccak__keccak_round_key63 = Felt(
            cairo_obj.keccak__keccak__keccak_round_key63
        )
        self.poseidon__poseidon__full_round_key0 = Felt(
            cairo_obj.poseidon__poseidon__full_round_key0
        )
        self.poseidon__poseidon__full_round_key1 = Felt(
            cairo_obj.poseidon__poseidon__full_round_key1
        )
        self.poseidon__poseidon__full_round_key2 = Felt(
            cairo_obj.poseidon__poseidon__full_round_key2
        )
        self.poseidon__poseidon__partial_round_key0 = Felt(
            cairo_obj.poseidon__poseidon__partial_round_key0
        )
        self.poseidon__poseidon__partial_round_key1 = Felt(
            cairo_obj.poseidon__poseidon__partial_round_key1
        )
        self.memory__multi_column_perm__perm__interaction_elm = Felt(
            cairo_obj.memory__multi_column_perm__perm__interaction_elm
        )
        self.memory__multi_column_perm__hash_interaction_elm0 = Felt(
            cairo_obj.memory__multi_column_perm__hash_interaction_elm0
        )
        self.range_check16__perm__interaction_elm = Felt(
            cairo_obj.range_check16__perm__interaction_elm
        )
        self.diluted_check__permutation__interaction_elm = Felt(
            cairo_obj.diluted_check__permutation__interaction_elm
        )
        self.diluted_check__interaction_z = Felt(cairo_obj.diluted_check__interaction_z)
        self.diluted_check__interaction_alpha = Felt(
            cairo_obj.diluted_check__interaction_alpha
        )
        self.memory__multi_column_perm__perm__public_memory_prod = Felt(
            cairo_obj.memory__multi_column_perm__perm__public_memory_prod
        )
        self.range_check16__perm__public_memory_prod = Felt(
            cairo_obj.range_check16__perm__public_memory_prod
        )
        self.diluted_check__first_elm = Felt(cairo_obj.diluted_check__first_elm)
        self.diluted_check__permutation__public_memory_prod = Felt(
            cairo_obj.diluted_check__permutation__public_memory_prod
        )
        self.diluted_check__final_cum_val = Felt(cairo_obj.diluted_check__final_cum_val)

    def __repr__(self) -> str:
        dict = {
            "trace_length": self.trace_length,
            "initial_pc": self.initial_pc,
            "final_pc": self.final_pc,
            "initial_ap": self.initial_ap,
            "final_ap": self.final_ap,
            "initial_pedersen_addr": self.initial_pedersen_addr,
            "initial_range_check_addr": self.initial_range_check_addr,
            "initial_ecdsa_addr": self.initial_ecdsa_addr,
            "initial_bitwise_addr": self.initial_bitwise_addr,
            "initial_ec_op_addr": self.initial_ec_op_addr,
            "initial_keccak_addr": self.initial_keccak_addr,
            "initial_poseidon_addr": self.initial_poseidon_addr,
            "range_check_min": self.range_check_min,
            "range_check_max": self.range_check_max,
            "offset_size": self.offset_size,
            "half_offset_size": self.half_offset_size,
            "pedersen__shift_point": self.pedersen__shift_point,
            "ecdsa__sig_config": self.ecdsa__sig_config,
            "ec_op__curve_config": self.ec_op__curve_config,
            "pedersen__points__x": self.pedersen__points__x,
            "pedersen__points__y": self.pedersen__points__y,
            "ecdsa__generator_points__x": self.ecdsa__generator_points__x,
            "ecdsa__generator_points__y": self.ecdsa__generator_points__y,
            "keccak__keccak__keccak_round_key0": self.keccak__keccak__keccak_round_key0,
            "keccak__keccak__keccak_round_key1": self.keccak__keccak__keccak_round_key1,
            "keccak__keccak__keccak_round_key3": self.keccak__keccak__keccak_round_key3,
            "keccak__keccak__keccak_round_key7": self.keccak__keccak__keccak_round_key7,
            "keccak__keccak__keccak_round_key15": self.keccak__keccak__keccak_round_key15,
            "keccak__keccak__keccak_round_key31": self.keccak__keccak__keccak_round_key31,
            "keccak__keccak__keccak_round_key63": self.keccak__keccak__keccak_round_key63,
            "poseidon__poseidon__full_round_key0": self.poseidon__poseidon__full_round_key0,
            "poseidon__poseidon__full_round_key1": self.poseidon__poseidon__full_round_key1,
            "poseidon__poseidon__full_round_key2": self.poseidon__poseidon__full_round_key2,
            "poseidon__poseidon__partial_round_key0": self.poseidon__poseidon__partial_round_key0,
            "poseidon__poseidon__partial_round_key1": self.poseidon__poseidon__partial_round_key1,
            "memory__multi_column_perm__perm__interaction_elm": self.memory__multi_column_perm__perm__interaction_elm,
            "memory__multi_column_perm__hash_interaction_elm0": self.memory__multi_column_perm__hash_interaction_elm0,
            "range_check16__perm__interaction_elm": self.range_check16__perm__interaction_elm,
            "diluted_check__permutation__interaction_elm": self.diluted_check__permutation__interaction_elm,
            "diluted_check__interaction_z": self.diluted_check__interaction_z,
            "diluted_check__interaction_alpha": self.diluted_check__interaction_alpha,
            "memory__multi_column_perm__perm__public_memory_prod": self.memory__multi_column_perm__perm__public_memory_prod,
            "range_check16__perm__public_memory_prod": self.range_check16__perm__public_memory_prod,
            "diluted_check__first_elm": self.diluted_check__first_elm,
            "diluted_check__permutation__public_memory_prod": self.diluted_check__permutation__public_memory_prod,
            "diluted_check__final_cum_val": self.diluted_check__final_cum_val,
        }
        return f"{dict}"
