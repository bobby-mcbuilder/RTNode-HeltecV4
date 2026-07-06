#pragma once

#include "Type.h"
#include <memory>

namespace RNS {
	// Stub — channel support removed. Retained for LinkData.h compatibility.
	class Channel {
	public:
		Channel(Type::NoneConstructor) {}
		Channel(const Channel&) = default;
		Channel& operator=(const Channel&) = default;
		operator bool() const { return false; }
		bool operator<(const Channel&) const { return false; }
		void _shutdown() {}
	};
	class ChannelAdvertisement {};
}
